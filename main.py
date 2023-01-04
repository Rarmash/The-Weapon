import discord
import os
import pymongo
from options import token, mongodb_link, datapath, timeoutpath, eventspath, debugmode
import os.path
import json

intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.messages = True

bot = discord.Bot(case_insensitive=True, intents=intents)

myclient = pymongo.MongoClient(mongodb_link)
Collection = myclient["Messages"]["Messages"]

if os.path.exists(datapath):
    os.remove(datapath)

for data in Collection.find({}, {'_id': 0}):
    with open(datapath, 'w+') as newsave:
        newsave.write(str(data).replace("'", '"'))

Collection1 = myclient["Messages"]["Timeouts"]

if os.path.exists(timeoutpath):
    os.remove(timeoutpath)

for data in Collection1.find({}, {'_id': 0}):
    with open(timeoutpath, 'w+') as newsave:
        newsave.write(str(data).replace("'", '"'))

Collection2 = myclient["Server"]["Events"]

if os.path.exists(eventspath):
    os.remove(eventspath)

for data in Collection2.find({}, {'_id': 0}):
    with open(eventspath, 'w+', encoding="utf8") as newsave:
        json.dump(data, newsave, indent=4, ensure_ascii=False)

myclient.close()

@bot.event
async def on_ready():
    print("------")
    print("Бот запущен!")
    print(f"Вошли как {bot.user.name}")
    print(f"ID бота: {str(bot.user.id)}")
    for guild in bot.guilds:
        print(f"Подключились к серверу: {guild}")
    print("------")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="за этой установкой"))


for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        if filename == "events.py" and debugmode == "ON":
            pass
        else:
            bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token)
