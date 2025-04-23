from discord.ext import commands, tasks
from discord import Embed, Color
from Database.daily_wire_articles import update_database, clearhtml
from Database.daily_wire_subscribe import *

class daily_wire_feeds(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.post_articles.start()
        self.check_for_new_articles.start()
        self.new_articles = []

    @tasks.loop(minutes=3)
    async def check_for_new_articles(self):
        articles = await update_database()
        new_articles = articles['new_feeds']
        updated_articles = articles['updated_feeds']  
        if new_articles:
            self.new_articles = [(i['title'],
                i['author'],
                i['link'],
                clearhtml(i['content'][0]['value'])) for i in new_articles]

    @tasks.loop(minutes=3)
    async def post_articles(self):
        try:
            with open('SERVERPARAMS') as f:
                server_params = json.load(f)
                channel_id = server_params['databases']['daily_wire']['channel']
            channel = await self.bot.fetch_channel(channel_id)
        except:
            print("channel not found")
            return None
        
        while(self.new_articles):
            res = self.new_articles.pop(0)
            embed = Embed(title=res[0], url=res[2], description=res[3][0:500],
                            color=Color.blue())
            embed.set_author(name=res[1], url = "https://www.dailywire.com/author/" + res[1].replace(' ', '-'))
            members = get_subscribers_with_match(res[0])
            members.extend(get_subscribers_with_author(res[1]))
            for member in members:
                user = await self.bot.fetch_user(member)
                if not user:
                    continue
                await user.send(embed=embed)
            await channel.send(embed=embed, delete_after=604800)

    @commands.group(name="subscribe", help="DM's you Daily Wire Articles that match author or keywords of your choice")
    async def subscribe_daily_wire_articles(self, ctx: commands.context):
        if ctx.invoked_subcommand is None:
            pass

    @subscribe_daily_wire_articles.group(name='keywords', help='DM daily wire articles that have keywords in title')
    async def subscribe_daily_wire_articles_tags(self, ctx: commands.context):
        if ctx.invoked_subcommand is None:
            member_id = ctx.author.id
            result = get_keywords(member_id)
            msg = f'You are subscribed to the following keywords: {", ".join(result)}' if result else 'You are not subscribed to any keywords.'
            await ctx.send(msg)

    @subscribe_daily_wire_articles_tags.command(name="add", help = 'Adds the keyword')
    async def subscribe_daily_wire_articles_tags_add(self, ctx: commands.context, *args):
        member_id = ctx.author.id
        keyword = ' '.join(args) if len(args) > 1 else args[0]
        add_keyword(member_id, keyword)
        await ctx.send('Added ' + keyword + ' keyword to subscription filter.')

    @subscribe_daily_wire_articles_tags.command(name="remove", help = 'Removes the keyword')
    async def subscribe_daily_wire_articles_tags_remove(self, ctx: commands.context, *args):
        member_id = ctx.author.id
        keyword = ' '.join(args) if len(args) > 1 else args[0]
        remove_keyword(member_id, keyword)
        await ctx.send('Remove ' + keyword + ' keyword from subscription filter.')

    @subscribe_daily_wire_articles.group(name='authors', help = 'DM daily wire articles by author')
    async def subscribe_daily_wire_articles_author(self, ctx: commands.context):
        if ctx.invoked_subcommand is None:
            member_id = ctx.author.id
            result = get_author(member_id)
            msg = f'You are subscribed to the following authors: {", ".join(result)}' if result else 'You are not subscribed to any authors.'
            await ctx.send(msg)

    @subscribe_daily_wire_articles_author.command(name="add", help = "Adds an author")
    async def subscribe_daily_wire_articles_author_add(self, ctx: commands.context, *args):
        member_id = ctx.author.id
        authors = ' '.join(args) if len(args) > 1 else args[0]
        add_author(member_id, authors)
        await ctx.send('Added ' + authors + ' author to subscription.')

    @subscribe_daily_wire_articles_author.command(name="remove", help = "Removes an author")
    async def subscribe_daily_wire_articles_author_remove(self, ctx: commands.context, *args):
        member_id = ctx.author.id
        authors = ' '.join(args) if len(args) > 1 else args[0]
        remove_author(member_id, authors)
        await ctx.send('Removed ' + authors + ' author from subscription.')


async def setup(bot: commands.Bot):
    await bot.add_cog(daily_wire_feeds(bot))