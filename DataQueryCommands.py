
from discord.ext import commands
from discord import File, Embed, Color
from Data import *
from dailywirequery import query_daily_wire

class data_query_commands(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="kitten")
    async def kitten(self, ctx: commands.context):
        with open('Data/kitten_blog.jpg', 'rb') as f:
            picture = File(f)
            await ctx.send(file=picture)

    @commands.command(name="puppy")
    async def kitten(self, ctx: commands.context):
        with open('Data/dog.jpg', 'rb') as f:
            picture = File(f)
            await ctx.send(file=picture)

    @commands.command(name="police_shootings", help='To query, type {from year, to year, column a, column b, ...} from available columns Year,White_armed,White_unarmed,Black_armed,Black_unarmed,Hispanic_armed,Hispanic_unarmed,A_armed,N_armed,O_armed,NA_armed,N_unarmed,O_unarmed,A_unarmed,NA_unarmed')
    async def get_police_shooting_data(self, ctx: commands.context, *args):
        res = querypoliceshooting(*args)
        save_df_as_matplotlib_plot(res, 'dataimg.jpg')
        with open('dataimg.jpg', 'rb') as f:
            picture = File(f)
            await ctx.send(file=picture)

    @commands.command(name="covid_statistics")
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

    @commands.command(name="find_articles")
    async def find_daily_wire_articles(self, ctx: commands.context, *args):
        query = args[0]
        results = query_daily_wire(query)
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