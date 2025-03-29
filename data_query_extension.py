import datetime

from discord import File, Embed
from discord.ext import commands

from Database.data_queries import query_covid_statistics, querypoliceshooting, save_df_as_matplotlib_graph, save_df_as_matplotlib_plot

class DataQuery(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="police_shootings", help='To query, type {from year, to year, column a, column b, ...} from available columns Year,White_armed,White_unarmed,Black_armed,Black_unarmed,Hispanic_armed,Hispanic_unarmed,A_armed,N_armed,O_armed,NA_armed,N_unarmed,O_unarmed,A_unarmed,NA_unarmed')
    async def get_police_shooting_data(self, ctx: commands.context, *args):
        res = querypoliceshooting(*args)
        save_df_as_matplotlib_plot(res, 'dataimg.jpg')
        with open('dataimg.jpg', 'rb') as f:
            picture = File(f)
            await ctx.send(file=picture)

    @commands.command(name="covid_statistics", help='type: {imageplot,imagetable} country[US] startdate[year-month-day] enddate[year-month-day] {new_cases,new_deaths}')
    async def covid_statistics(self, ctx, *args):
        if len(args) == 3:
            outputtype = args[0]
            country = args[1]
            startdate = datetime.datetime.strptime(args[2], "%Y-%m-%d")
            enddate = datetime.datetime.strptime(args[3], "%Y-%m-%d")
        else:
            outputtype = 'imageplot'
            country = "USA"
            startdate = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
            now = datetime.datetime.now()
            enddate = datetime.datetime.strptime(f"{now.year}-{now.month}-{now.day}", "%Y-%m-%d")
        if len(args) >= 4:
            columns = [x.lower() for x in list(args[4:len(args)])]
        else:
            columns = ['new_cases']
        await ctx.send("Aquiring Data...")
        data = query_covid_statistics(country, startdate, enddate, columns)
        if outputtype == 'texttable':
            await ctx.send(data)
        elif outputtype == 'imagetable':
            save_df_as_matplotlib_plot(data, 'Data/covid.jpg')
            with open('Data/covid.jpg', 'rb') as f:
                image = File(f)
                await ctx.send(file=image)
        elif outputtype == 'imageplot':
            await ctx.send("Generating plot...")
            save_df_as_matplotlib_graph(data, 'Data/covid.jpg')
            with open('Data/covid.jpg', 'rb') as f:
                image = File(f)
                embed = Embed()
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
                await ctx.send(embed=embed)
                await ctx.send(file=image)

async def setup(bot: commands.Bot):
    await bot.add_cog(DataQuery(bot))