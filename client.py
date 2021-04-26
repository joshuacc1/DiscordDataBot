import discord
import pandas
from bokeh.io import export_png, export_svgs
from bokeh.models import ColumnDataSource, DataTable, TableColumn
import matplotlib.pyplot as plt

from discord.ext import commands


#client = discord.Client()
GUILD = "Prometheus's server"

bot = commands.Bot(command_prefix='#%')

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

@bot.command(name='kitten')
async def kitten(ctx):
    with open('Data/kitten_blog.jpg', 'rb') as f:
        picture=discord.File(f)
        await ctx.send(file=picture)


@bot.command(name='get_data')
async def getdata(ctx,arg1 : int,arg2 : int):
    print(arg1,arg2)
    x=[1,2,3,4,5,6]
    output=x[arg1:arg2]
    await ctx.send(' '.join([str(x) for x in output]))

@bot.command(name='police_shootings',help='To query, type {from year, to year, column a, column b, ...} from available columns White_armed,White_unarmed,black_armed,black_unarmed,Hispanic_armed,Hispanic_unarmed,A_armed,N_armed,O_armed,NA_armed,N_unarmed,O_unarmed,A_unarmed,NA_unarmed')
async def get_police_shooting_data(ctx,*args):
    res=querypoliceshooting(*args)
    save_df_as_matplotlib_plot(res, 'dataimg.jpg')
    with open('dataimg.jpg', 'rb') as f:
        picture=discord.File(f)
        await ctx.send(file=picture)
    #await ctx.send('That data given may indicate a different conclusion than any preconception you may have. in any case... here is your data:' + '\n' + res.to_string(index=False,justify='center') + '\n' + 'Facts dont care about your feelings')

def querypoliceshooting(*args):
    iyear=int(args[0])
    fyear=int(args[1])
    df = pandas.read_csv('Data/Police_Shootings_By_Race.csv')
    if len(args) >=3:
        columns=list(args[2:len(args)])
        columns.insert(0,'Year')
        if all(x in df.columns for x in columns):
            res = df[columns][df['Year']>=iyear][df['Year']<=fyear]
    else:
        res=df[df['Year']>=iyear][df['Year']<=fyear]

    print(res)
    save_df_as_matplotlib_plot(res, 'dataimg.png')
    return res

def save_df_as_image(df,path):
    source=ColumnDataSource(df)
    df_columns=[df.index.name]
    df_columns.extend(df.columns.values)
    columns_for_table=[]
    for column in df_columns:
        columns_for_table.append(TableColumn(field=column,title=column))

    data_table=DataTable(source=source,columns=columns_for_table,height_policy='auto',width_policy='auto',index_position=None)
    export_png(data_table,filename=path)

def save_df_as_matplotlib_plot(df,path):
    fig,ax=plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=df.values,colLabels=df.columns,loc='center',cellLoc='center',colColours=['gray']*len(df.columns))
    fig.tight_layout()
    plt.savefig(path)


if __name__=="__main__":
    pass
    #print(querypoliceshooting(2018,2020,'White_armed'))

bot.run('ODM0NjE0MjgyMjU5OTIyOTc0.YIDdHw.xBCMT9FrtayUrFEY8f9FzltdN2w')
#client.run('ODM0NjE0MjgyMjU5OTIyOTc0.YIDdHw.xBCMT9FrtayUrFEY8f9FzltdN2w')