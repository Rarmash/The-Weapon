from options import token as discordToken
from options import log_channel as logger
import discord
from discord.ext import commands
from bannedChannels import bannedChannels
from bannedUsers import bannedUsers

intents = discord.Intents.default()
intents.members=True
intents.messages=True

bot = commands.Bot(command_prefix='?', case_insensitive=True)

@bot.event
async def on_ready():
    print("------")
    print("Bot is ready!")
    print("Logged in as: " + bot.user.name)
    print("Bot ID: " + str(bot.user.id))
    for guild in bot.guilds:
        print ("Connected to server: {}".format(guild))
    print("------")
    await bot.change_presence(activity=discord.Game('Halo Infinite Battle Royale'))

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
    embed.set_footer(text = "Powered by R4")
    if (ctx.channel.id not in bannedChannels) and (ctx.author.id not in bannedUsers):
        await channel.send(embed = embed)
    
bot.run(discordToken)