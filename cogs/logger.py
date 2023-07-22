import discord
from discord.ext import commands
from options import servers_data, myclient
import io

class Logger(commands.Cog):
    def __init__(self, bot, servers_data):
        self.bot = bot
        self.servers_data = servers_data

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        server_data = self.servers_data.get(str(ctx.guild.id))
        if not server_data:
            return
        channel = self.bot.get_channel(server_data.get("log_channel"))
        author = ctx.author.id
        Collection = myclient[f"{str(ctx.guild.id)}"]["Users"]
        if ctx.channel.id in server_data.get("bannedChannels", []) or author in server_data.get("bannedUsers", []) or ctx.channel.category_id in server_data.get("bannedCategories", []):
            return
        user = Collection.find_one({"_id": str(author)})
        if user:
            Collection.update_one({"_id": str(author)}, {"$set": {"messages": user.get("messages", 0) - 1}})
        else:
            Collection.insert_one({"_id": str(author), "messages": -1, "timeouts": 0})
        embed = discord.Embed(
            title='Удалённое сообщение',
            description=ctx.content,
            color=int(server_data.get("accent_color"), 16)
        )
        embed.add_field(
            name='Автор',
            value=f'<@{author}>'
        )
        embed.add_field(
            name='Канал',
            value=f'<#{ctx.channel.id}>'
        )
        for attach in ctx.attachments:
            imgn = attach.filename
            img = io.BytesIO(await attach.read())
        try:
            await channel.send(file = discord.File(img, imgn), embed=embed)
        except UnboundLocalError:
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        guild_id = str(before.guild.id)
        server_data = self.servers_data.get(guild_id)
        if not server_data:
            return
        if before.channel.id in server_data.get("bannedChannels", []) or before in server_data.get("bannedUsers", []) or before.channel.category_id in server_data.get("bannedCategories", []) or before.content == after.content:
            return
        channel = self.bot.get_channel(server_data.get("log_channel"))
        embed = discord.Embed(
            color=int(server_data.get("accent_color"), 16)
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
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Logger(bot, servers_data))
