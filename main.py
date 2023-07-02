import discord
import os
from options import token, debugmode, version
import os.path

intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.messages = True

bot = discord.Bot(case_insensitive=True, intents=intents)

status = ['In the Library', 'Killing Flood', 'Dodging Spartan Lasers']

@bot.event
async def on_ready():
    print("------")
    print("Бот запущен!")
    print(f"Версия: {version}")
    print(f"Вошли как {bot.user.name}")
    print(f"ID бота: {str(bot.user.id)}")
    for guild in bot.guilds:
        print(f"Подключились к серверу: {guild}")
    print("------")
    if debugmode == "OFF":
        status = discord.Status.online
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"за этой установкой (v{version})")
    else:
        status = discord.Status.dnd
        activity = discord.Activity(type=discord.ActivityType.competing, name=f"debug-режиме (v{version})")
    await bot.change_presence(status=status, activity=activity)


for filename in os.listdir("./cogs"):
    if (
        filename.endswith(".py")
        and filename != "__init__.py"
        and (filename != "events.py" or debugmode != "ON")
    ):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token)
