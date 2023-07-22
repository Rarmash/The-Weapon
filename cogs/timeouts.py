from discord.ext import commands
from options import myclient

class Timeouts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        Collection = myclient[f"{str(before.guild.id)}"]["Users"]
        if after.timed_out:
            author = str(after.id)
            timeoutCount = Collection.find_one({"_id": author})
            if timeoutCount is None:
                timeoutCount = {"_id": author, "timeouts": 1}
                Collection.insert_one(timeoutCount)
            else:
                timeoutCount["timeouts"] += 1
                Collection.update_one({"_id": author}, {"$set": {"timeouts": timeoutCount["timeouts"]}})

def setup(bot):
    bot.add_cog(Timeouts(bot))
