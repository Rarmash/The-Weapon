import json
import discord
from discord.ext import commands
from options import mongodb_link, timeoutpath, accent_color
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
                    
    @commands.slash_command(description='Посмотреть таблицу лидеров по тайм-аутам')
    async def timeoutleaderboard(self, ctx):
        with open(timeoutpath, 'r') as file:
            leaderboard = json.load(file)
        user_ids = list(leaderboard.keys())
        user_message_counts = list(leaderboard.values())
        new_leaderboard = []
        for index, user_id in enumerate(user_ids, 1):
            new_leaderboard.append([user_id, user_message_counts[index - 1]])
        new_leaderboard.sort(key=lambda items: items[1], reverse=True)
        desk = ''
        kolvo = 0
        for users in new_leaderboard:
            desk += f'<@{users[0]}>: {users[1]}\n'
            kolvo += int(users[1])
        embed = discord.Embed(title='Лидеры по тайм-аутам',
                              description=desk, color=accent_color)
        embed.set_footer(text=f"Всего получено {kolvo} тайм-аутов")
        await ctx.respond(embed=embed)
def setup(bot):
    bot.add_cog(Timeouts(bot))
