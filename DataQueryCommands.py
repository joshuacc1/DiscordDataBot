import os
import re
from random import choice

from discord.ext import commands
from discord import File, Embed, Color
from Data import *
from dailywirequery import query_daily_wire

class data_query_commands(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

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

    @commands.command(name="pets", help = 'This bot will show pictures of your pet.\n\n'
                                         'Bot will pick a random pet without any commands\n\n'
                                         'Add your pet with the picture\n'
                                         'add {pet name} {attach file}\n\n'
                                         'Get the tagged members pets\n'
                                         '{tag member}\n'
                                         'owner {tag member}\n\n'
                                         'Get all your pet pictures.\n'
                                         'mypets')
    async def dwcpet(self, ctx: commands.context, *args):
        if args:
            if args[0].lower() == "add":
                if not len(args) >= 2:
                    await ctx.send("Please specify your pets name. i.e. #%dwcpet add bingo")
                else:
                    if ctx.message.attachments:
                        _types = ['png','gif','jpg']
                        if not all([any([x.filename.endswith(_type) for _type in _types]) for x in ctx.message.attachments]):
                            await ctx.send("Please send png, jpg, or gif files only.")
                        else:
                            if args[1] == 'tagowner':
                                owner = str(re.search('<@!(.*)>', args[2]).group(1))
                                petname = ' '.join(args[4:])
                            else:
                                owner = str(ctx.message.author.id)
                                petname = ' '.join(args[1:])
                            for attachment in ctx.message.attachments:
                                if '%%' in attachment.filename:
                                    fname = attachment.filename.replace('%%', '')
                                else:
                                    fname = attachment.filename

                                await attachment.save(os.getcwd() + '/Data/Pets/' + owner + '%%' + petname + '%%' + fname)
                                await ctx.send('Successfully uploaded pet!')

            if args[0].lower() == 'owner':
                if not len(args) == 2:
                    await ctx.send("Please specify the pet owners name. i.e. #%dwcpet owner john")
                else:
                    if args[1].startswith('<@'):
                        taggedowner = str(re.search('<@(.*)>',args[1]).group(1))
                        if taggedowner.startswith('!'):
                            taggedowner = taggedowner[1:]
                    else:
                        taggedowner = ''
                    results = self.query_file(taggedowner)
                    for result in results:
                        await ctx.send('Meet ' + result[1], file=result[0])

            if args[0].lower() == 'mypets':
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

            if args[0].startswith('<@'):
                taggedowner = str(re.search('<@(.*)>', args[0]).group(1))
                if taggedowner.startswith('!'):
                    taggedowner = taggedowner[1:]
                results = self.query_file(taggedowner)
                for result in results:
                    await ctx.send('Meet ' + result[1], file=result[0])
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

    def query_file(self, taggedowner):
        res = []
        filenames = os.listdir(os.getcwd() + "/Data/Pets")
        for filename in filenames:
            info = filename.split('%%')
            if len(info) >= 3:
                ownerid = info[0]
                petname = info[1]
                if ownerid == taggedowner:
                    f = open("Data/Pets/" + filename, 'rb')
                    picture = File(f)
                    res.append((picture,petname))
        return res


    @commands.command(name="police_shootings", help='To query, type {from year, to year, column a, column b, ...} from available columns Year,White_armed,White_unarmed,Black_armed,Black_unarmed,Hispanic_armed,Hispanic_unarmed,A_armed,N_armed,O_armed,NA_armed,N_unarmed,O_unarmed,A_unarmed,NA_unarmed')
    async def get_police_shooting_data(self, ctx: commands.context, *args):
        res = querypoliceshooting(*args)
        save_df_as_matplotlib_plot(res, 'dataimg.jpg')
        with open('dataimg.jpg', 'rb') as f:
            picture = File(f)
            await ctx.send(file=picture)

    @commands.command(name="covid_statistics", help='type: {imageplot,imagetable} country[US] startdate[year-month-day] enddate[year-month-day] {new_cases,new_deaths}')
    async def covid_statistics(self, ctx, *args):
        outputtype = args[0]
        country = args[1]
        startdate = datetime.datetime.strptime(args[2], "%Y-%m-%d")
        enddate = datetime.datetime.strptime(args[3], "%Y-%m-%d")
        if len(args) >= 4:
            columns = [x.lower() for x in list(args[4:len(args)])]
        else:
            columns = ['new_cases']
        data = query_covid_statistics(country, startdate, enddate, columns)
        if outputtype == 'texttable':
            await ctx.send(data)
        elif outputtype == 'imagetable':
            save_df_as_matplotlib_plot(data, 'Data/covid.jpg')
            with open('Data/covid.jpg', 'rb') as f:
                image = File(f)
                await ctx.send(file=image)
        elif outputtype == 'imageplot':
            save_df_as_matplotlib_graph(data, 'Data/covid.jpg')
            with open('Data/covid.jpg', 'rb') as f:
                image = File(f)
                embed = Embed()
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                await ctx.send(file=image)

    @commands.command(name="dw", help = 'Type #%dw {search phrase} to search any daily wire articels')
    async def find_daily_wire_articles(self, ctx: commands.context, *args):
        if len(args) == 1:
            query = args[0]
        else:
            query = ' '.join(args)

        results = query_daily_wire(query,database = 'file')
        if results:
            for res in results[0:2]:
                embed = Embed(title=res[0], url=res[2], description=res[3][0:500],
                              color=Color.blue())
                embed.set_author(name=res[1], url = "https://www.dailywire.com/author/" + res[1].replace(' ', '-'))
                await ctx.send(embed=embed)
        else:
            await ctx.send("No good articles found.")

    @commands.Bot.listen
    async def on_message(self, message):
        if message.author == self.bot.user:
            return None
        print(message.author, message.content, self.bot.user)
        if message.content.startswith('George Floyd'):
            await message.channel.send('George Floyd deserved to die!')
        await self.bot.process_commands(message)

def setup(bot: commands.Bot):
    bot.add_cog(data_query_commands(bot))