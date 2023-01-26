import json
import discord
from discord.ext import commands
from options import mongodb_link, admin_channel, userpath, accent_color
import datetime
from math import ceil
import time
import pymongo

myclient = pymongo.MongoClient(mongodb_link)
Collection = myclient["Server"]["Users"]

messageCount = json.load(open(userpath, 'r'))

class MessagesCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        with open(userpath, 'r') as file:
            messageCount = json.load(file)
            author = str(ctx.author.id)
        if not ctx.author.bot and ctx.channel.id != 940736668661600326:
            if author in messageCount:
                messageCount[author][u"messages"] += 1
            else:
                entry = {author: {
                    "messages": 1,
                    "timeouts": 0
                }}
                messageCount.update(entry)
            with open(userpath, 'w') as update_file:
                json.dump(messageCount, update_file, indent=4)
                Collection.delete_many({})
                if isinstance(messageCount, list):
                    Collection.insert_many(messageCount)
                else:
                    Collection.insert_one(messageCount)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        date_format = "%#d.%#m.%Y в %H:%M:%S"
        with open(userpath) as file:
            file_data = json.load(file)
        channel = self.bot.get_channel(admin_channel)
        with open(userpath, 'r') as file:
            messageCount = json.load(file)
            author = str(member.id)
        embed = discord.Embed(
            description=f"<@{author}> ({member.display_name}) вышел с сервера.",
            color=accent_color
        )
        embed.add_field(name="Дата захода на сервер", value=f"<t:{ceil(time.mktime((datetime.datetime.strptime(str(member.joined_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S')+datetime.timedelta(hours=3)).timetuple()))}:f>")
        embed.add_field(name="Сообщений", value=file_data[str(member.id)][u"messages"])
        embed.add_field(name="Таймаутов", value=file_data[str(member.id)][u"timeouts"])
        await channel.send(embed=embed)
        if not member.bot:
            if author in messageCount:
                if messageCount[author][u"timeouts"] == 0:
                    del messageCount[author]
                else:
                    messageCount[author][u"messages"] = 0
            with open(userpath, 'w') as update_file:
                json.dump(messageCount, update_file, indent=4)
                Collection.delete_many({})
                if isinstance(file_data, list):
                    Collection.insert_many(file_data)
                else:
                    Collection.insert_one(file_data)
    
def setup(bot):
    bot.add_cog(MessagesCounter(bot))
