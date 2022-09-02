import json
import discord
from discord.ext import commands
from options import mongodb_link, timeoutpath
import pymongo

myclient = pymongo.MongoClient(mongodb_link)
Collection = myclient["Messages"]["Timeouts"]

try:
    timeoutCount = json.load(open(timeoutpath, 'r'))
except:
    with open(timeoutpath, 'w+') as newsave:
        newsave.write('{}')
    timeoutCount = json.load(open(timeoutpath, 'r'))

class Timeouts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.timed_out:
            with open(timeoutpath, 'r') as file:
                timeoutCount = json.load(file)
                author = str(after.id)
            if author in timeoutCount:
                timeoutCount[author] += 1
            else:
                timeoutCount[author] = 1
            with open(timeoutpath, 'w') as update_file:
                json.dump(timeoutCount, update_file, indent=4)
                Collection.delete_many({})
                if isinstance(timeoutCount, list):
                    Collection.insert_many(timeoutCount)
                else:
                    Collection.insert_one(timeoutCount)

def setup(bot):
    bot.add_cog(Timeouts(bot))
