import json
import discord
from discord.ext import commands
from options import mongodb_link, admin_channel, userpath, accent_color
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
        with open(userpath) as file:
            file_data = json.load(file)
        with open(userpath, 'r') as file:
            messageCount = json.load(file)
            author = str(member.id)
        if not member.bot:
            if author in messageCount:
                del messageCount[author]
            with open(userpath, 'w') as update_file:
                json.dump(messageCount, update_file, indent=4)
                Collection.delete_many({})
                if isinstance(file_data, list):
                    Collection.insert_many(file_data)
                else:
                    Collection.insert_one(file_data)
        channel = self.bot.get_channel(admin_channel)
        embed = discord.Embed(
            description=f'<@{author}> ({member.display_name}) вышел с сервера.',
            color=accent_color
        )
        await channel.send(embed=embed)
    
def setup(bot):
    bot.add_cog(MessagesCounter(bot))
