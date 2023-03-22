import discord
import os
from options import token, debugmode
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
    print(f"Вошли как {bot.user.name}")
    print(f"ID бота: {str(bot.user.id)}")
    for guild in bot.guilds:
        print(f"Подключились к серверу: {guild}")
    print("------")
    if debugmode == "OFF":
        status = discord.Status.online
    else:
        status = discord.Status.dnd
    await bot.change_presence(status=status, activity=discord.Activity(type=discord.ActivityType.watching, name="за этой установкой"))


for filename in os.listdir("./cogs"):
    if (
        filename.endswith(".py")
        and filename != "__init__.py"
        and (filename != "events.py" or debugmode != "ON")
    ):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token)
