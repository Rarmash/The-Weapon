from options import token as discordToken
from options import admin_id as administrator
import discord
import os
import pymongo
from options import mongodb_link

intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.messages = True

bot = discord.Bot(case_insensitive=True, intents=intents)

myclient = pymongo.MongoClient(mongodb_link)
db = myclient["Messages"]
Collection = db["Messages"]

for data in Collection.find({}, {'_id': 0}):
    with open('data.json', 'w+') as newsave:
        newsave.write(str(data).replace("'", '"'))

myclient.close()


@bot.event
async def on_ready():
    print("------")
    print("Бот запущен!")
    print(f"Вошли как {bot.user.name}")
    print(f"ID бота: {str(bot.user.id)}")
    for guild in bot.guilds:
        my_server = bot.get_server('982338827580485632')
        await bot.leave_server(my_server)
        print(f"Подключились к серверу: {guild}")
    print("------")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="за этой установкой"))

cogs = bot.create_group("service", "Сервисные команды")

@cogs.command()
async def unload(ctx, extension):
    if ctx.author.id == administrator:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.respond(f"**cogs.{extension}** выгружается...")
    else:
        await ctx.respond("Недостаточно прав для выполнения данной команды.")


@cogs.command()
async def load(ctx, extension):
    if ctx.author.id == administrator:
        bot.load_extension(f"cogs.{extension}")
        await ctx.respond(f"**cogs.{extension}** запускается...")
    else:
        await ctx.respond("Недостаточно прав для выполнения данной команды.")


@cogs.command()
async def reload(ctx, extension):
    if ctx.author.id == administrator:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.respond(f"**cogs.{extension}** перезапускается...")
    else:
        await ctx.respond("Недостаточно прав для выполнения данной команды.")
        
for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(discordToken)
