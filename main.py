import discord
import os
from options import token, debugmode, version, myclient
import os.path

# Define intents for the bot to receive all available events
intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.messages = True

# Create the Discord bot instance with specified intents
bot = discord.Bot(case_insensitive=True, intents=intents)

# Gears are always cool

# Event that runs when the bot is ready and connected to Discord
@bot.event
async def on_ready():
    # Connect to the MongoDB server
    myclient
    
    # Print bot information and connected guilds
    print("------")
    print(f"{bot.user.name} запущен!")
    print(f"Версия: {version}")
    print(f"ID бота: {str(bot.user.id)}")
    for guild in bot.guilds:
        print(f"Подключились к серверу: {guild}")
    print("------")
    
    # Set bot status and activity based on debugmode
    if debugmode == "ON":
        status = discord.Status.dnd
        activity = discord.Activity(type=discord.ActivityType.playing, name=f"debug-режиме (v{version})")
    else:
        status = discord.Status.online
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"за этой установкой (v{version})")
    await bot.change_presence(status=status, activity=activity)
    
# Load cog extensions
for filename in os.listdir("./cogs"):
    if (
        filename.endswith(".py")
        and filename != "__init__.py"
        and (filename != "events.py" or debugmode != "ON")
    ):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Run the bot with the provided token
bot.run(token)
