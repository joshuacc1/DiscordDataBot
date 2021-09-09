import sys

import discord
# import matplotlib.dates
# import pandas
# import numpy
# from bokeh.io import export_png, export_svgs
# from bokeh.models import ColumnDataSource, DataTable, TableColumn
# import matplotlib.pyplot as plt
# import json
# import urllib.request
# import datetime

from discord.ext import commands
from Database.DatabaseManagement import messagesmanagement
from dailywirequery import query_daily_wire, query_dailywire_paragraphs
from discord import Embed, Color

client = discord.Client()
GUILD = "Prometheus's server"
TOKEN = ''

# intents = discord.Intents.default()
# intents.members = True
bot = commands.Bot(command_prefix='#%')

bot.load_extension('DataQueryCommands')
# @client.event
# async def on_ready():
#     print('we have logged in as {0.user}'.format(client))
#     guild = discord.utils.get(client.guilds,name=GUILD)
#
#     print(f'{client.user} is connected to the following guild\n'
#           f'{guild.name}(id: {guild.id})')
#
#
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')
#
# @bot.command(name='kitten')
# async def kitten(ctx):
#     with open('Data/kitten_blog.jpg', 'rb') as f:
#         picture=discord.File(f)
#         await ctx.send(file=picture)
#
# @bot.command(name='police_shootings',help='To query, type {from year, to year, column a, column b, ...} from available columns Year,White_armed,White_unarmed,Black_armed,Black_unarmed,Hispanic_armed,Hispanic_unarmed,A_armed,N_armed,O_armed,NA_armed,N_unarmed,O_unarmed,A_unarmed,NA_unarmed')
# async def get_police_shooting_data(ctx,*args):
#     res=querypoliceshooting(*args)
#     save_df_as_matplotlib_plot(res, 'dataimg.jpg')
#     with open('dataimg.jpg', 'rb') as f:
#         picture=discord.File(f)
#         await ctx.send(file=picture)
#     #await ctx.send('That data given may indicate a different conclusion than any preconception you may have. in any case... here is your data:' + '\n' + res.to_string(index=False,justify='center') + '\n' + 'Facts dont care about your feelings')
#
# @bot.command(name='covid_statistics')
# async def covid_statistics(ctx,*args):
#     outputtype=args[0]
#     country=args[1]
#     startdate=datetime.datetime.strptime(args[2],"%Y-%m-%d")
#     enddate=datetime.datetime.strptime(args[3],"%Y-%m-%d")
#     if len(args) >= 4:
#         columns=[x.lower() for x in list(args[4:len(args)])]
#     else:
#         columns=['new_cases']
#     data=query_covid_statistics(country,startdate,enddate,columns)
#     if outputtype=='texttable':
#         await ctx.send(data)
#     elif outputtype=='imagetable':
#         save_df_as_matplotlib_plot(data,'Data/covid.jpg')
#         with open('Data/covid.jpg','rb') as f:
#             image=discord.File(f)
#             await ctx.send(file=image)
#     elif outputtype=='imageplot':
#         save_df_as_matplotlib_graph(data,'Data/covid.jpg')
#         with open('Data/covid.jpg','rb') as f:
#             image=discord.File(f)
#             embed=discord.Embed()
#             embed.set_author(name=ctx.author.display_name,icon_url=ctx.author.avatar_url)
#             await ctx.send(embed=embed)
#             await ctx.send(file=image)
#
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return None
    mm = messagesmanagement()
    mm.addmessage(message)

    # print(message.id, message.author, message.content, message.guild.name, message.channel, message.reference)
    # if message.reference:
    #     print(message.reference.message_id
    #       ,message.reference.channel_id,message.reference.guild_id, message.reference.resolved.content)
    await bot.process_commands(message)
    # results = query_dailywire_paragraphs(message.content,database = 'file',strength = 0.1)
    # if results:
    #     await message.channel.send(str(message.author) + " said something that reminded me of a dailywire articles: ")
    #     for res in results[0:2]:
    #         embed = Embed(title=res[0], url=res[2], description=res[3][0:500],
    #                       color=Color.blue())
    #         embed.set_author(name=res[1], url="https://www.dailywire.com/author/" + res[1].replace(' ', '-'))
    #         await message.channel.send(embed=embed)

    # if message.content.startswith('George Floyd'):
    #     await message.channel.send('George Floyd deserved to die!')
    # await bot.process_commands(message)


def main(args):
    TOKENKEYFILE=args[1]
    with open(TOKENKEYFILE, 'r') as f:
        global TOKEN
        TOKEN = f.readline()
    bot.run(TOKEN)

if __name__=="__main__":
    main(sys.argv)
    #res=querypoliceshooting(2018,2020,'white_armed','black_armed','white_unarmed','black_unarmed')
    #print(res)
    # save_df_as_matplotlib_plot(res,'dataimage.jpg')
    # sdate=datetime.datetime(2020,3,1)
    # edate=datetime.datetime(2021,4,26)
    # data=query_covid_statistics('USA',sdate,edate,['new_cases','new_deaths'])
    # save_df_as_matplotlib_graph(data, 'dataimage.jpg')
    #main(['','TOKEN'])
#main(sys.argv)
#client.run(TOKEN)
#main(['','TOKEN'])