from options import token as discordToken
from options import log_channel as logger
from options import admin_id as administrator
import discord
from discord.ext import commands
from bannedChannels import bannedChannels
from bannedUsers import bannedUsers
import os

intents = discord.Intents.all()
intents.presences = True
intents.members=True
intents.messages=True

bot = commands.Bot(command_prefix='!', case_insensitive=True, presences = True)

@bot.event
async def on_ready():
    print("------")
    print("Бот запущен!")
    print(f"Вошли как {bot.user.name}")
    print(f"ID бота: {str(bot.user.id)}")
    for guild in bot.guilds:
        print(f"Подключились к серверу: {guild}")
    print("------")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="за этой установкой"))

@bot.event
async def on_message_delete(ctx):
    channel = bot.get_channel(logger)
    embed = discord.Embed(
        title = 'Удалённое сообщение',
        description = ctx.content,
        color = 0x209af8
    )
    embed.add_field(
        name = 'Автор',
        value = f'<@{ctx.author.id}>'
    )
    embed.add_field(
        name = 'Канал',
        value = f'<#{ctx.channel.id}>'
    )
    if (ctx.channel.id not in bannedChannels) and (ctx.author.id not in bannedUsers) and (str(ctx.content)[0] != '!')  and (not ctx.author.bot):
        await channel.send(embed = embed)
        
@bot.event
async def on_message_edit(before, after):
    channel = bot.get_channel(logger)
    embed = discord.Embed(
        color = 0x209af8
        )
    embed.add_field(
        name = "Редактированное сообщение",
        value = after.content,
        inline=False
        )
    embed.add_field(
        name = "Оригинальное сообщение",
        value = before.content,
        inline=False
        )
    embed.add_field(
        name = 'Автор',
        value = f'<@{before.author.id}>'
    )
    embed.add_field(
        name = 'Канал',
        value = f'<#{before.channel.id}>'
    )
    if (before.channel.id not in bannedChannels) and (before.author.id not in bannedUsers) and (str(before.content)[0] != '!')  and (not before.author.bot) and (before.content != after.content):
        await channel.send(embed = embed)
        
@bot.command()
async def unload(ctx, extension):
    if ctx.author.id == administrator:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send("Ког выгружается...")
    else:
        await ctx.send("Недостаточно прав для выполнения данной команды.")


@bot.command()
async def load(ctx, extension):
    if ctx.author.id == administrator:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("Ког запускается...")
    else:
        await ctx.send("Недостаточно прав для выполнения данной команды.")


@bot.command()
async def reload(ctx, extension):
    if ctx.author.id == administrator:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("Ког перезапускается...")
    else:
        await ctx.send("Недостаточно прав для выполнения данной команды.")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f'cogs.{filename[:-3]}')
    
bot.run(discordToken)