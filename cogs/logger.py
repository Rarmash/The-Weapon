import discord
from discord.ext import commands
from ignoreList import bannedChannels, bannedUsers, bannedCategories
from options import log_channel, accent_color, Collection
import io

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        channel = self.bot.get_channel(log_channel)
        author = ctx.author.id
        embed = discord.Embed(
            title='Удалённое сообщение',
            description=ctx.content,
            color=accent_color
        )
        embed.add_field(
            name='Автор',
            value=f'<@{author}>'
        )
        embed.add_field(
            name='Канал',
            value=f'<#{ctx.channel.id}>'
        )
        if (ctx.channel.id not in bannedChannels) and (author not in bannedUsers) and (not ctx.author.bot) and (ctx.channel.category_id not in bannedCategories):
            for attach in ctx.attachments:
                imgn = attach.filename
                img = io.BytesIO(await attach.read())
            try:
                await channel.send(file = discord.File(img, imgn), embed=embed)
            except UnboundLocalError:
                await channel.send(embed=embed)
        user = Collection.find_one({"_id": str(author)})
        if user:
            messages = user.get("messages", 0) - 1
            Collection.update_one({"_id": str(author)}, {"$set": {"messages": messages}})
        else:
            Collection.insert_one({"_id": str(author), "messages": -1, "timeouts": 0})

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
