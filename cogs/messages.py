import discord
from discord.ext import commands
from options import myclient, servers_data
import datetime
from math import ceil
import time

class MessagesCounter(commands.Cog):
    def __init__(self, bot, servers_data):
        self.bot = bot
        self.servers_data = servers_data

    @commands.Cog.listener()
    async def on_message(self, ctx):
        author = str(ctx.author.id)
        server_data = self.servers_data.get(str(ctx.guild.id))
        if not server_data:
            return
        Collection = myclient[f"{str(ctx.guild.id)}"]["Users"]
        if not ctx.author.bot and ctx.channel.id not in server_data.get("trash_channels", []):
            user = Collection.find_one({"_id": author})
            if user:
                messages = user.get("messages", 0) + 1
                Collection.update_one({"_id": author}, {"$set": {"messages": messages}})
            else:
                Collection.insert_one({"_id": author, "messages": 1, "timeouts": 0})
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        server_data = self.servers_data.get(str(member.guild.id))
        if not server_data:
            return
        Collection = myclient[f"{str(member.guild.id)}"]["Users"]
        date_format = "%#d.%#m.%Y в %H:%M:%S"
        user = Collection.find_one({"_id": str(member.id)})
        channel = self.bot.get_channel(server_data.get("admin_channel"))
        if user:
            embed = discord.Embed(
                description=f"<@{user['_id']}> ({member.display_name}) вышел с сервера.",
                color=int(server_data.get("accent_color"), 16)
            )
            embed.add_field(name="Дата захода на сервер", value=f"<t:{ceil(time.mktime((datetime.datetime.strptime(str(member.joined_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S')+datetime.timedelta(hours=3)).timetuple()))}:f>")
            embed.add_field(name="Сообщений", value=user.get("messages", 0))
            embed.add_field(name="Таймаутов", value=user.get("timeouts", 0))
            if user["timeouts"] == 0:
                Collection.delete_one({"_id": str(member.id)})
            else:
                Collection.update_one({"_id": str(member.id)}, {"$set": {"messages": 0}})
            await channel.send(embed=embed)
    
def setup(bot):
    bot.add_cog(MessagesCounter(bot, servers_data))
