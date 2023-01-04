import json
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import mongodb_link, userpath, accent_color
import pymongo

myclient = pymongo.MongoClient(mongodb_link)
Collection = myclient["Server"]["Users"]

counters = json.load(open(userpath, 'r'))

class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    leaderboardcmd = SlashCommandGroup("leaderboard", "Лидерборды")
    
    @leaderboardcmd.command(description='Посмотреть таблицу лидеров по тайм-аутам')
    async def timeouts(self, ctx):
        with open(userpath, 'r') as file:
            leaderboard = json.load(file)
        user_ids = list(leaderboard.keys())
        user_message_counts = []
        for i in leaderboard:
            user_message_counts.append(leaderboard[i][u"timeouts"])
        new_leaderboard = []
        for index, user_id in enumerate(user_ids, 1):
            if user_message_counts[index - 1] != 0:
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
        with open(userpath, 'r') as file:
            leaderboard = json.load(file)
        user_ids = list(leaderboard.keys())
        user_message_counts = []
        for i in leaderboard:
            user_message_counts.append(leaderboard[i][u"messages"])
        new_leaderboard = []
        for index, user_id in enumerate(user_ids, 1):
            new_leaderboard.append([user_id, user_message_counts[index - 1]])
        new_leaderboard.sort(key=lambda items: items[1], reverse=True)
        desk = ''
        kolvo, k = 0, 0
        for users in new_leaderboard:
            k += 1
            if k == 1:
                desk += f'🥇 <@{users[0]}>: {users[1]}\n'
            elif k == 2:
                desk += f'🥈 <@{users[0]}>: {users[1]}\n'
            elif k == 3:
                desk += f'🥉 <@{users[0]}>: {users[1]}\n'
            else:
                desk += f'{k}. <@{users[0]}>: {users[1]}\n'
            kolvo += int(users[1])
            if k >= 10:
                break
        embed = discord.Embed(title='Лидеры по сообщениям',
                              description=desk, color=accent_color)
        user = str(ctx.author.id)
        k = 0
        place10 = 0
        urplace = 0
        for users in new_leaderboard:
            k+=1
            if k == 10:
                place10 = users[1]
            if users[0] == user and k>10:
                embed.add_field(name="Ваше положение в таблице", value=f'{k}. <@{users[0]}>: {users[1]}\n')
                urplace = users[1]
                break
        if k<=10 or k == len(new_leaderboard):
            embed.set_footer(text=f"Всего отправлено {kolvo} сообщений")
        else:
            embed.set_footer(text=f"Вам осталось {place10-urplace+1} сообщений до 10-го места")
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Leaderboards(bot))
