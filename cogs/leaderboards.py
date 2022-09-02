import json
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import mongodb_link, timeoutpath, datapath, accent_color
import pymongo

myclient = pymongo.MongoClient(mongodb_link)
Collection = myclient["Messages"]["Timeouts"]

try:
    timeoutCount = json.load(open(timeoutpath, 'r'))
except:
    with open(timeoutpath, 'w+') as newsave:
        newsave.write('{}')
    timeoutCount = json.load(open(timeoutpath, 'r'))

Collection = myclient["Messages"]["Messages"]

try:
    messageCount = json.load(open(datapath, 'r'))
except:
    with open(datapath, 'w+') as newsave:
        newsave.write('{}')
    messageCount = json.load(open(datapath, 'r'))

class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    leaderboardcmd = SlashCommandGroup("leaderboard", "Лидерборды")
    
    @leaderboardcmd.command(description='Посмотреть таблицу лидеров по тайм-аутам')
    async def timeouts(self, ctx):
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
        
    @leaderboardcmd.command(description='Посмотреть таблицу лидеров по сообщениям')
    async def messages(self, ctx):
        with open(datapath, 'r') as file:
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
        embed = discord.Embed(title='Лидеры по сообщениям',
                              description=desk, color=accent_color)
        embed.set_footer(text=f"Всего отправлено {kolvo} сообщений")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Leaderboards(bot))
