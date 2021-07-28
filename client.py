import sys

import discord
import matplotlib.dates
import pandas
import numpy
from bokeh.io import export_png, export_svgs
from bokeh.models import ColumnDataSource, DataTable, TableColumn
import matplotlib.pyplot as plt
import json
import urllib.request
import datetime

from discord.ext import commands


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
    print(message.author, message.content, bot.user, client.guilds)
    if message.content.startswith('George Floyd'):
        await message.channel.send('George Floyd deserved to die!')
    await bot.process_commands(message)
#
# def querypoliceshooting(*args):
#     iyear=int(args[0])
#     fyear=int(args[1])
#     df = pandas.read_csv('Data/Police_Shootings_By_Race.csv')
#     if len(args) >=3:
#         columns=list(args[2:len(args)])
#         columns.insert(0,'Year')
#         ttable=[x.lower() in [y.lower() for y in columns] for x in df.columns]
#         table=df.columns[ttable]
#         print(table)
#         #if all(x in df.columns for x in columns):
#         res = df[table][df['Year']>=iyear][df['Year']<=fyear]
#     else:
#         res=df[df['Year']>=iyear][df['Year']<=fyear]
#
#     print(res)
#     save_df_as_matplotlib_plot(res, 'dataimg.png')
#     return res
#
# def query_covid_statistics(country,sdate,edate,columns):
#     with urllib.request.urlopen('https://covid.ourworldindata.org/data/owid-covid-data.json') as url:
#         data=json.loads(url.read().decode())
#
#     def columnvalue(item,col,default):
#         if col in item:
#             return item[col]
#         else:
#             return default
#     dataquery={'date':[]}
#     for col in columns:
#         dataquery[col]=[]
#     for x in data[country]['data']:
#         date=[int(w) for w in x['date'].split('-')]
#         linedate=datetime.datetime(date[0],date[1],date[2])
#         if linedate>=sdate and linedate<edate:
#             for col in dataquery:
#                 dataquery[col].append(columnvalue(x,col,None))
#     data=pandas.DataFrame(dataquery)
#     return data
#
# def save_df_as_image(df,path):
#     source=ColumnDataSource(df)
#     df_columns=[df.index.name]
#     df_columns.extend(df.columns.values)
#     columns_for_table=[]
#     for column in df_columns:
#         columns_for_table.append(TableColumn(field=column,title=column))
#
#     data_table=DataTable(source=source,columns=columns_for_table,height_policy='auto',width_policy='auto',index_position=None)
#     export_png(data_table,filename=path)
#
# def save_df_as_matplotlib_plot(df,path):
#     fig,ax=plt.subplots()
#     fig.patch.set_visible(False)
#     ax.axis('off')
#     ax.axis('tight')
#     ax.table(cellText=df.values,colLabels=df.columns,loc='center',cellLoc='center',colColours=['gray']*len(df.columns))
#     fig.tight_layout()
#     plt.savefig(path)
#     #plt.show()
#
# def save_df_as_matplotlib_graph(df,path):
#     fig,ax=plt.subplots()
#     fig.patch.set_visible(False)
#     daterange = [datetime.datetime.strptime(x, "%Y-%m-%d").date() for x in df['date']]
#     for col in df.columns[1:]:
#         ax.plot(daterange,[x for x in df[col]],label=col)
#     intv=(daterange[-1]-daterange[0])/10
#     ax.xaxis.set_major_locator(matplotlib.dates.DayLocator(interval=intv.days))
#     ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m-%d-%Y"))
#     ax.tick_params(axis='x',labelrotation=90)
#     fig.tight_layout()
#     plt.savefig(path)
#     #plt.show()

def main(args):
    TOKENKEYFILE=args[1]
    with open(TOKENKEYFILE, 'r') as f:
        global TOKEN
        TOKEN = f.readline()
    bot.run(TOKEN)

if __name__=="__main__":
    pass
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
main(['','TOKEN'])