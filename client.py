import sys
import json

import discord
import tracemalloc

from discord.ext import commands
from Database.messages import addmessage

tracemalloc.start()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(intents=intents, command_prefix='$$')

@bot.event
async def on_ready():
    await bot.load_extension('pets_extension')
    await bot.load_extension('daily_wire_extension')
    await bot.load_extension('data_query_extension')
    synced = await bot.tree.sync()  # Sync slash commands with Discord
    print(f"Synced commands: {[command.name for command in synced]}")  # Debugging
    print("loaded Extensions")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return None
    if message.reference:
        refmessdict = {'message_id': message.reference.message_id,
                        'channel_id': message.reference.channel_id,
                        'guild_id': message.reference.guild_id}
        if message.reference.resolved:
            refmessdict['reply_message'] = message.reference.resolved.content
    else:
        refmessdict = {}

    addmessage(message.id, str(message.author),message.content,str(message.guild),str(message.channel),refmessdict)
    await bot.process_commands(message)

def main(args):
    with open("SERVERPARAMS",'r') as f:
        server_params = json.load(f)
        TOKEN = server_params['token']
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