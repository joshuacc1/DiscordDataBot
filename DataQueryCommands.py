import os
import re
import time
from random import choice

from discord.ext import commands, tasks
from discord import File, Embed, Color
from Data import *
from dailywirequery import query_daily_wire, update_database, clearhtml
from Database.DatabaseManagement import MemberManagement

PUBLISH_CHANNEL_ID = 849639790571421746

class data_query_commands(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.post_articles.start()

    @tasks.loop(minutes=1)
    async def post_articles(self):
        try:
            channel = await self.bot.fetch_channel(PUBLISH_CHANNEL_ID)
        except:
            return None
        MM = MemberManagement()
        new_articles, update_articles = update_database()
        results = [(i['title'],
                i['author'],
                i['link'],
                clearhtml(i['content'][0]['value'])) for i in new_articles]
        if results:
            for res in results:
                embed = Embed(title=res[0], url=res[2], description=res[3][0:500],
                                color=Color.blue())
                embed.set_author(name=res[1], url = "https://www.dailywire.com/author/" + res[1].replace(' ', '-'))
                for subscriber in MM.service_database('Daily_Wire'):
                    if 'author' in subscriber:
                        authorflag = any([author.lower() in res[1].lower() for author in  subscriber['author']])
                    else:
                        authorflag = False

                    if 'tags' in subscriber:
                        tagsflag = any([tag.lower() in res[0].lower() for tag in  subscriber['tags']])
                    else:
                        tagsflag = False

                    if tagsflag or authorflag:
                        user = await self.bot.fetch_user(subscriber['member'])
                        if not user:
                            continue
                        await user.send(embed=embed)
                await channel.send(embed=embed, delete_after=604800)

    @post_articles.before_loop
    async def post_post_articles(self):
        await self.bot.wait_until_ready()

    @commands.command(name='xp_item')
    async def respond_to_mee6(self, ctx: commands.context, *args):
        #if ctx.message.author.id == 851246358559981608:
        amount = args[1]
        if args[0].startswith('<@'):
            taggedowner = str(re.search('<@(.*)>', args[0]).group(1))
            if taggedowner.startswith('!'):
                taggedowner = int(taggedowner[1:])
        member = await ctx.guild.fetch_member(taggedowner)
        await ctx.send(f"!give_xp {member.mention} {amount}")


    
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

    @commands.group(name="subscribe", help="DM's you Daily Wire Articles that match author or keywords of your choice")
    async def subscribe_daily_wire_articles(self, ctx: commands.context):
        if ctx.invoked_subcommand is None:
            pass

    @subscribe_daily_wire_articles.group(name='keywords', help='DM daily wire articles that have keywords in title')
    async def subscribe_daily_wire_articles_tags(self, ctx: commands.context):
        if ctx.invoked_subcommand is None:
            member_id = ctx.author.id
            MM = MemberManagement()
            result = MM.get_service(member_id,'Daily_Wire')
            await ctx.send(', '.join(result['tags']))



    @subscribe_daily_wire_articles_tags.command(name="add", help = 'Adds the keyword')
    async def subscribe_daily_wire_articles_tags_add(self, ctx: commands.context, *args):
        member_id = ctx.author.id
        keyword = ' '.join(args) if len(args) > 1 else args[0]
        MM = MemberManagement()
        MM.add_service(member_id,'Daily_Wire', {'$addToSet': {'tags': keyword}})
        await ctx.send('Added ' + keyword + ' keyword to subscription filter.')

    @subscribe_daily_wire_articles_tags.command(name="remove", help = 'Removes the keyword')
    async def subscribe_daily_wire_articles_tags_remove(self, ctx: commands.context, *args):
        member_id = ctx.author.id
        keyword = ' '.join(args) if len(args) > 1 else args[0]
        MM = MemberManagement()
        MM.add_service(member_id,'Daily_Wire', {'$pull': {'tags': keyword}})
        await ctx.send('Remove ' + keyword + ' keyword from subscription filter.')

    @subscribe_daily_wire_articles.group(name='author', help = 'DM daily wire articles by author')
    async def subscribe_daily_wire_articles_author(self, ctx: commands.context):
        if ctx.invoked_subcommand is None:
            member_id = ctx.author.id
            MM = MemberManagement()
            result = MM.get_service(member_id,'Daily_Wire')
            await ctx.send(', '.join(result['author']))

    @subscribe_daily_wire_articles_author.command(name="add", help = "Adds an author")
    async def subscribe_daily_wire_articles_author_add(self, ctx: commands.context, *args):
        member_id = ctx.author.id
        keyword = ' '.join(args) if len(args) > 1 else args[0]
        MM = MemberManagement()
        MM.add_service(member_id,'Daily_Wire', {'$addToSet': {'author': keyword}})
        await ctx.send('Added ' + keyword + ' author to subscription.')

    @subscribe_daily_wire_articles_author.command(name="remove", help = "Removes an author")
    async def subscribe_daily_wire_articles_author_remove(self, ctx: commands.context, *args):
        member_id = ctx.author.id
        keyword = ' '.join(args) if len(args) > 1 else args[0]
        MM = MemberManagement()
        MM.add_service(member_id,'Daily_Wire', {'$pull': {'author': keyword}})
        await ctx.send('Removed ' + keyword + ' author from subscription.')

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

async def setup(bot: commands.Bot):
    await bot.add_cog(data_query_commands(bot))
