import discord
from discord.ext import commands, tasks
from discord import app_commands
import Fonctions2 as f
import asyncio
import datetime

serveur = 'ID of the discord server' 
ID = 'ID of the X/Twitter account'
channel_id = 'ID of the discord channel where the tweets will be posted'
TOKEN = 'TOKEN of the bot'
id_of_ok_users = ['id1', 'id2', 'id3'] #ID of the users who can use the bot

serveur_obj = discord.Object(id = serveur)

intents = discord.Intents().all()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

enable = False 
f.init(ID)
with open('ErrLogs.txt', 'w') as file : file.close()

def right(interaction : discord.Interaction):
    if interaction.user.id in id_of_ok_users :
        return True
    else:
        return False

@bot.event
async def on_ready():
    print("Bot launched :)")

    try:
        synced = await bot.tree.sync(guild=serveur_obj)
        print(f"{len(synced)} commands(s) synchronized")

    except Exception as e:
        print(e)

@tasks.loop(minutes = 5)
async def verifNewTweet() :
    try :
        tweet = await asyncio.to_thread(f.newTweet, ID)
    except Exception as e:
        now = datetime.datetime.now()
        with open('ErrLogs.txt', 'a') as file :
            file.write(f'{now.strftime("%d/%m/%Y %H:%M")} --> {e}\n')
            file.close()
        print(e)
        return
    
    else :
        print(f'New tweet : {tweet}')
        channel = bot.get_channel(channel_id)
        
        if tweet[0] :
            for url in reversed(tweet[1]) :
                await channel.send("New tweet !\n" + f.addFx(url))

@bot.tree.command(
    guild = serveur_obj,
    name = "activetwitter",
    description = "Enable automatic retrieval of tweets",
)
@app_commands.describe(enable = "Enable or disable")
async def members(interaction: discord.Interaction, enable : bool = True) :
    if not right(interaction) : await interaction.response.send_message(content = "Bro..don't try it.", ephemeral=True)
    if enable : 
        await interaction.response.send_message(content = "Automatic retrieval of tweets : `enabled`", ephemeral=True)
        await verifNewTweet.start() #start task line 37
    else : 
        await interaction.response.send_message(content = "Automatic retrieval of tweets : `disabled`", ephemeral=True)
        verifNewTweet.cancel()
        
@bot.tree.command(
    guild = serveur_obj,
    name = "see_files",
    description = "Send a file containing error logs and tweets data",
)
async def error(interaction: discord.Interaction) :
    if not right(interaction) : return
    await interaction.response.send_message(files = [discord.File('ErrLogs.txt'), discord.File('TweetsData.txt')], ephemeral = True)

bot.run(TOKEN)