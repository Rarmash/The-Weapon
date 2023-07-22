import discord
import os
from options import token, debugmode, version, myclient
import os.path

intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.messages = True

bot = discord.Bot(case_insensitive=True, intents=intents)

# Gears are always cool

@bot.event
async def on_ready():
    myclient
    print("------")
    print(f"{bot.user.name} запущен!")
    print(f"Версия: {version}")
    print(f"ID бота: {str(bot.user.id)}")
    for guild in bot.guilds:
        print(f"Подключились к серверу: {guild}")
    print("------")
    if debugmode == "ON":
        status = discord.Status.dnd
        activity = discord.Activity(type=discord.ActivityType.playing, name=f"debug-режиме (v{version})")
    else:
        status = discord.Status.online
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"за этой установкой (v{version})")
    await bot.change_presence(status=status, activity=activity)
    
for filename in os.listdir("./cogs"):
    if (
        filename.endswith(".py")
        and filename != "__init__.py"
        and (filename != "events.py" or debugmode != "ON")
    ):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token)
