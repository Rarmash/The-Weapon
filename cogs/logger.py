import discord
from discord.ext import commands
from ignoreList import bannedChannels, bannedUsers, bannedCategories
from options import mongodb_link, datapath, log_channel, accent_color
import pymongo
import json
import io

myclient = pymongo.MongoClient(mongodb_link)
Collection = myclient["Messages"]["Messages"]

messageCount = json.load(open(datapath, 'r'))

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        channel = self.bot.get_channel(log_channel)
        embed = discord.Embed(
            title='Удалённое сообщение',
            description=ctx.content,
            color=accent_color
        )
        embed.add_field(
            name='Автор',
            value=f'<@{ctx.author.id}>'
        )
        embed.add_field(
            name='Канал',
            value=f'<#{ctx.channel.id}>'
        )
        if (ctx.channel.id not in bannedChannels) and (ctx.author.id not in bannedUsers) and (not ctx.author.bot) and (ctx.channel.category_id not in bannedCategories):
            for attach in ctx.attachments:
                imgn = attach.filename
                img = io.BytesIO(await attach.read())
            try:
                await channel.send(file = discord.File(img, imgn), embed=embed)
            except UnboundLocalError:
                await channel.send(embed=embed)
        with open(datapath, 'r') as file:
            messageCount = json.load(file)
            author = str(ctx.author.id)
        if not ctx.author.bot:
            messageCount[author] -= 1
        with open(datapath, 'w') as update_file:
            json.dump(messageCount, update_file, indent=4)
            Collection.delete_many({})
            if isinstance(messageCount, list):
                Collection.insert_many(messageCount)
            else:
                Collection.insert_one(messageCount)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = self.bot.get_channel(log_channel)
        embed = discord.Embed(
            color=accent_color
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
        if (before.channel.id not in bannedChannels) and (before.author.id not in bannedUsers) and (not before.author.bot) and (before.content != after.content) and (before.channel.category_id not in bannedCategories):
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Logger(bot))
