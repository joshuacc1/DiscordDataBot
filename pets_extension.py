import os
import re
import time
from random import choice
import discord
from discord import File, Embed, Color, Interaction, Message, TextStyle, ButtonStyle
from discord.ui import TextInput, Modal, Button, View

from discord.ext import commands

from pet_image_generator import pictures_into_tiles_owner, get_files_in_folder

class AddPetModal(Modal):
    def __init__(self, bot: commands.Bot):
        super().__init__(title="Add a Pet")
        self.bot = bot

        # Add input fields to the modal
        self.add_item(TextInput(label="Pet Name", placeholder="Enter your pet's name"))
        self.add_item(TextInput(label="Pet Type", placeholder="e.g., Dog, Cat, etc."))
        self.add_item(TextInput(label="(optional) Pet Story", placeholder="Tell us something about your pet", style=TextStyle.long, required=False))

    async def on_submit(self, interaction: Interaction):
        print("callback called")
        # Get the input values from the modal
        pet_name = self.children[0].value
        pet_type = self.children[1].value
        pet_description = self.children[2].value

        print(pet_name,pet_type,pet_description)
        # Save the metadata temporarily (you can use a database instead)
        self.bot.pet_metadata[interaction.user.id] = {
            "pet_name": pet_name,
            "pet_type": pet_type,
            "pet_description": pet_description
        }

        # Prompt the user to upload a file
        await interaction.response.send_message(
            "Thank you! Now please upload a picture of your pet as an attachment in this channel.",
            ephemeral=True
        )

class AddPetButtonView(View):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="Add Pet", style=discord.ButtonStyle.primary)
    async def add_pet_button(self, interaction: Interaction, button: Button):
        """Callback for the button to open the modal."""
        modal = AddPetModal(self.bot)
        await interaction.response.send_modal(modal)

class pets(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.bot.pet_metadata = {}  # Temporary storage for pet metadata

    @commands.command(name="addpetform", help="Opens a form to add a pet.")
    async def add_pet_form(self, ctx: commands.Context):
        """Command to send a button that opens the modal form for adding a pet."""
        view = AddPetButtonView(self.bot)
        await ctx.send("Click the button below to add a pet:", view=view)

    @discord.ui.button(label="Add Pet", style=ButtonStyle.primary)
    async def add_pet_button(self, button: Button, interaction: Interaction):
        """Callback for the button to open the modal."""
        modal = AddPetModal(self.bot)
        await interaction.response.send_modal(modal)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Listener to handle file uploads after the modal."""
        if message.author.bot:
            return

        # Check if the user has pending metadata
        if message.author.id in self.bot.pet_metadata:
            # Ensure the user has attached a file
            if not message.attachments:
                await message.channel.send("Please attach a picture of your pet!")
                return

            # Validate the file type
            valid_types = ['png', 'jpg', 'jpeg', 'gif']
            attachment = message.attachments[0]
            if not any(attachment.filename.lower().endswith(ext) for ext in valid_types):
                await message.channel.send("Invalid file type! Please upload a PNG, JPG, or GIF file.")
                return

            # Save the file and metadata
            metadata = self.bot.pet_metadata.pop(message.author.id)
            pet_name = metadata["pet_name"]
            owner_id = str(message.author.id)
            file_path = f"Data/Pets/{owner_id}%%{pet_name}%%{attachment.filename}"

            # Save the file locally
            await attachment.save(file_path)

            # Respond to the user
            await message.channel.send(f"Successfully added your pet '{pet_name}'!", file=File(file_path))

    def query_file(self, taggedowner):
        res = []
        filenames = os.listdir(os.getcwd() + "/Data/Pets")
        for filename in filenames:
            info = filename.split('%%')
            if len(info) >= 3:
                ownerid = info[0]
                petname = info[1]
                if ownerid == taggedowner:
                    res.append(("Data/Pets/" + filename, petname))
        return res

    @commands.command(name="kitten", help = 'Posts a picture of a kitten.')
    async def kitten(self, ctx: commands.context):
        filenames = os.listdir(os.getcwd() + "\\Data\\Kittens")
        filechoice = choice(filenames)
        with open('Data/Kittens/' + filechoice, 'rb') as f:
            picture = File(f)
            await ctx.send(file=picture)

    @commands.command(name="puppy", help = 'Posts a picture of a puppy')
    async def puppy(self, ctx: commands.context):
        filenames = os.listdir(os.getcwd() + "\\Data\\Puppies")
        filechoice = choice(filenames)
        with open('Data/Puppies/' + filechoice, 'rb') as f:
            picture = File(f)
            await ctx.send(file=picture)

    @commands.group(name="pets", help = 'This bot will show pictures of your pet.\n\n'
                                            'Bot will pick a random pet without any commands\n\n'
                                            'To get tagged members pets:\n'
                                            '#%testpets {tag member}')
    async def dwcpet(self, ctx: commands.context):
        sub_command = ctx.subcommand_passed if ctx.subcommand_passed else ''
        if ctx.invoked_subcommand is None:
            if sub_command.startswith('<@'):
                taggedowner = str(re.search('<@(.*)>', sub_command).group(1))
                if taggedowner.startswith('!'):
                    taggedowner = taggedowner[1:]
                print(taggedowner)
                owner = 'No Name'
                for member in ctx.guild.members:
                    if str(member.id) == taggedowner:
                        owner = member.display_name
                
                filenames = get_files_in_folder("Data/Pets")
                files = [x for x in filenames if str(taggedowner) in x]
                print(files)
                buffer = pictures_into_tiles_owner(owner,files)
                print(buffer)
                picture = discord.File(buffer, filename="labeled_grid.png")
                await ctx.send("", file=picture)

                # results = self.query_file(taggedowner)
                # for result in results:
                #     with open(result[0], 'rb') as f:
                #         picture = File(f)
                #         await ctx.send('Meet ' + result[1], file=picture)
            else:
                filenames = os.listdir(os.getcwd() + "/Data/Pets")
                filechoice = choice(filenames)
                info = filechoice.split('%%')
                petname = ''
                owner = ''
                if len(info) >= 3:
                    petname = info[1]
                    ownerid = info[0]
                    for member in ctx.message.guild.members:
                        if str(member.id) == ownerid:
                            owner = member.display_name
                with open('Data/Pets/' + filechoice, 'rb') as f:
                    picture = File(f)
                    hstr = ''
                    if petname:
                        hstr += 'Meet ' + petname
                        if owner:
                            hstr += ' who\'s owned by ' + owner
                        await ctx.send(hstr)
                    await ctx.send(file=picture)

    @dwcpet.command(name='add', help='Add your pet with the picture\n'
                                     'add {pet name} {attach file}\n')
    async def pets_add(self, ctx: commands.context, *args):
        if not len(args) >= 1:
            await ctx.send("Please specify your pets name. i.e. #%dwcpet add bingo")
        else:
            if ctx.message.attachments:
                _types = ['png', 'gif', 'jpg']
                if not all([any([x.filename.endswith(_type) for _type in _types]) for x in ctx.message.attachments]):
                    await ctx.send("Please send png, jpg, or gif files only.")
                else:
                    if args[0] == 'ownerid':
                        owner = args[1]
                        petname = ' '.join(args[2:])
                    else:
                        owner = str(ctx.message.author.id)
                        petname = ' '.join(args[0:])

                    for attachment in ctx.message.attachments:
                        if '%%' in attachment.filename:
                            fname = attachment.filename.replace('%%', '')
                        else:
                            fname = attachment.filename

                        await attachment.save(os.getcwd() + '/Data/Pets/' + owner + '%%' + petname + '%%' + fname)
                        await ctx.send('Successfully uploaded pet!')

    # @dwcpet.command(name='mypets', help = 'Get all your pet pictures.\n')
    # async def pets_mypets(self, ctx: commands.context):
    #     filenames = os.listdir(os.getcwd() + "/Data/Pets")
    #     filternames = []
    #     for filename in filenames:
    #         info = filename.split('%%')
    #         if len(info) >= 3:
    #             ownerid = info[0]
    #             petname = info[1]
    #             if ownerid == str(ctx.message.author.id):
    #                 filternames.append(filename)
    #                 f = open("Data/Pets/" + filename, 'rb')
    #                 picture = File(f)
    #                 await ctx.send('Meet ' + petname, file=picture)

    @dwcpet.command(name='mypets', help = 'Get all your pet pictures.\n')
    async def pets_mypets(self, ctx: commands.context):
        filenames = get_files_in_folder("Data/Pets")
        files = [x for x in filenames if str(ctx.message.author.id) in x]
        print(files)
        buffer = pictures_into_tiles_owner(ctx.author.display_name,files)
        print(buffer)
        picture = discord.File(buffer, filename="labeled_grid.png")
        await ctx.send("", file=picture)
        # for filename in filenames:
        #     info = filename.split('%%')
        #     if len(info) >= 3:
        #         ownerid = info[0]
        #         petname = info[1]
        #         files.append({'filepath':filename,'petname':info[1],'owner':info[0]})
        # picture_count = len(files)

    @dwcpet.command(name = 'owner', help = 'Get the tagged members pets\n'
                                           '{tag member}\n'
                                           'owner {tag member}\n')
    async def pets_owner(self, ctx: commands.context, *args):
        if not len(args) == 2:
            await ctx.send("Please specify the pet owners name. i.e. #%dwcpet owner john")
        else:
            if args[1].startswith('<@'):
                taggedowner = str(re.search('<@(.*)>', args[1]).group(1))
                if taggedowner.startswith('!'):
                    taggedowner = taggedowner[1:]
            else:
                taggedowner = ''
            results = self.query_file(taggedowner)
            for result in results:
                with open(result[0], 'rb') as f:
                    picture = File(f)
                    await ctx.send('Meet ' + result[1], file=picture)

    @dwcpet.command(name = 'remove', help = 'Removes the pictures of your pet:\n'
                                            '#%pets remove {petname}')
    async def pets_remove(self, ctx: commands.context, *args):
        if args:
            petname = ' '.join(args)
            owner = str(ctx.message.author.id)
            results = self.query_file(owner)
            print(results)
            for result in results:
                if result[1] == petname:
                    with open(result[0], 'rb') as f:
                        picture = File(f)
                        await ctx.send('removing ' + petname, file=picture)
                    os.remove(result[0])
        else:
            await ctx.send('Please specify the pet name for pictures you want to remove')

async def setup(bot: commands.Bot):
    await bot.add_cog(pets(bot))