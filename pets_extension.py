import os
import re
import time
from random import choice
from discord import File, Embed, Color

from discord.ext import commands

class pets(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

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
                results = self.query_file(taggedowner)
                for result in results:
                    with open(result[0], 'rb') as f:
                        picture = File(f)
                        await ctx.send('Meet ' + result[1], file=picture)
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

    @dwcpet.command(name='mypets', help = 'Get all your pet pictures.\n')
    async def pets_mypets(self, ctx: commands.context):
        filenames = os.listdir(os.getcwd() + "/Data/Pets")
        filternames = []
        for filename in filenames:
            info = filename.split('%%')
            if len(info) >= 3:
                ownerid = info[0]
                petname = info[1]
                if ownerid == str(ctx.message.author.id):
                    filternames.append(filename)
                    f = open("Data/Pets/" + filename, 'rb')
                    picture = File(f)
                    await ctx.send('Meet ' + petname, file=picture)

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