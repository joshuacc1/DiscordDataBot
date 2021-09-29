import sys

import discord

from discord.ext import commands
from Database.DatabaseManagement import messagesmanagement

client = discord.Client()
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