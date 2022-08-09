import json
import discord
from discord.ext import commands
from options import mongodb_link, admin_channel
import pymongo
from math import ceil
import time
import datetime

myclient = pymongo.MongoClient(mongodb_link)
db = myclient["Messages"]
Collection = db["Messages"]

messageCount = json.load(open('data.json', 'r'))


class MessagesCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        with open('data.json') as file:
            file_data = json.load(file)
        with open('data.json', 'r') as file:
            messageCount = json.load(file)
            author = str(ctx.author.id)
        if not ctx.author.bot and ctx.channel.id != 940736668661600326:
            if author in messageCount:
                messageCount[author] += 1
            else:
                messageCount[author] = 1
            with open('data.json', 'w') as update_file:
                json.dump(messageCount, update_file, indent=4)
                Collection.delete_many({})
                if isinstance(file_data, list):
                    Collection.insert_many(file_data)
                else:
                    Collection.insert_one(file_data)

    @commands.slash_command(description='Посмотреть таблицу лидеров')
    async def leaderboard(self, ctx):
        with open('data.json', 'r') as file:
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
                              description=desk, color=0x209af8)
        # embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Всего отправлено {kolvo} сообщений")
        await ctx.respond(embed=embed)
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open('data.json') as file:
            file_data = json.load(file)
        with open('data.json', 'r') as file:
            messageCount = json.load(file)
            author = str(member.id)
        if not member.bot:
            if author in messageCount:
                del messageCount[author]
            with open('data.json', 'w') as update_file:
                json.dump(messageCount, update_file, indent=4)
                Collection.delete_many({})
                if isinstance(file_data, list):
                    Collection.insert_many(file_data)
                else:
                    Collection.insert_one(file_data)
        channel = self.bot.get_channel(admin_channel)
        date_format = "%#d.%#m.%Y в %H:%M:%S"
        embed = discord.Embed(
            description=f"<@{author}> ({member.display_name}) вышел с сервера.\nБыл на сервере с <t:{ceil(time.mktime(datetime.datetime.strptime(str(user.joined_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S').timetuple()))}:f>",
            color=0x209af8
        )
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(MessagesCounter(bot))
