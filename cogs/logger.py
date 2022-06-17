import discord
from discord.ext import commands
from bannedChannels import bannedChannels
from bannedUsers import bannedUsers
from options import log_channel as logger
from options import mongodb_link
import pymongo
import json


myclient = pymongo.MongoClient(mongodb_link)
db = myclient["Messages"]
Collection = db["Messages"]

messageCount = json.load(open('data.json', 'r'))

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        channel = self.bot.get_channel(logger)
        embed = discord.Embed(
            title='Удалённое сообщение',
            description=ctx.content,
            color=0x209af8
        )
        embed.add_field(
            name='Автор',
            value=f'<@{ctx.author.id}>'
        )
        embed.add_field(
            name='Канал',
            value=f'<#{ctx.channel.id}>'
        )
        if (ctx.channel.id not in bannedChannels) and (ctx.author.id not in bannedUsers) and (str(ctx.content)[0] != '!') and (not ctx.author.bot):
            await channel.send(embed=embed)
        with open('data.json') as file:
            file_data = json.load(file)
        with open('data.json', 'r') as file:
            messageCount = json.load(file)
            author = str(ctx.author.id)
        messageCount[author] -= 1
        with open('data.json', 'w') as update_file:
            json.dump(messageCount, update_file, indent=4)
            Collection.delete_many({})
            if isinstance(file_data, list):
                Collection.insert_many(file_data)
            else:
                Collection.insert_one(file_data)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = self.bot.get_channel(logger)
        embed = discord.Embed(
            color=0x209af8
        )
        embed.add_field(
            name="Редактированное сообщение",
            value=after.content,
            inline=False
        )
        embed.add_field(
            name="Оригинальное сообщение",
            value=before.content,
            inline=False
        )
        embed.add_field(
            name='Автор',
            value=f'<@{before.author.id}>'
        )
        embed.add_field(
            name='Канал',
            value=f'<#{before.channel.id}>'
        )
        if (before.channel.id not in bannedChannels) and (before.author.id not in bannedUsers) and (str(before.content)[0] != '!') and (not before.author.bot) and (before.content != after.content):
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Logger(bot))
