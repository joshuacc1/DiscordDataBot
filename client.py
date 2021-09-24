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
# GUILD = "Prometheus's server"
# TOKEN = ''

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix='#%')

bot.load_extension('DataQueryCommands')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return None
    mm = messagesmanagement()
    mm.addmessage(message)
    # if message.author.id == 564219418482311169:
    #     await message.channel.send("Mr. Markarama is the best")

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

import asyncio  # The only thing u need to import

#
# async def forever():
#     print('Task Complete')
#     await asyncio.sleep(15)
#
#
# bot.loop.create_task(forever())

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