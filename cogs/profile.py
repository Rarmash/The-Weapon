import json
import discord
from discord.ext import commands
import time
import datetime
from math import ceil
import sys
import platform
from options import admin_role_id, insider_id

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        date_format = "%#d.%#m.%Y в %H:%M:%S"
        if user is None:
            user = ctx.author
        if user.status == discord.Status.online:
            status = "🟢 в сети"
        if user.status == discord.Status.offline:
            status = "⚪ не в сети"
        if user.status == discord.Status.idle:
            status = "🌙 не активен"
        if user.status == discord.Status.dnd:
            status = "⛔ не беспокоить"
        with open('data.json') as json_file:
            json_data = json.load(json_file)
        for users in json_data:
            if int(users) == user.id:
                quantity = json_data[users]+1
        try:
            quantity
        except:
            quantity = 0
        if user.id != self.bot.user.id:
            embed = discord.Embed(title = f'Привет, я {user.name}', description=f"<@{user.id}> — {status}", color = 0x209af8)
            embed.add_field(name = "Регистрация", value = f"<t:{ceil(time.mktime(datetime.datetime.strptime(str(user.created_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S').timetuple()))}:f>")
            embed.add_field(name = "На сервере с", value = f"<t:{ceil(time.mktime(datetime.datetime.strptime(str(user.joined_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S').timetuple()))}:f>")
            embed.add_field(name = "Сообщений", value = quantity)
            if discord.utils.get(ctx.guild.roles, id=insider_id) in user.roles:
                embed.set_footer(text="Принимает участие в тестировании и помогает серверу стать лучше")
            if user.id == 415533286358777856:
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/964614960325992478/982716016184410122/4c8de376-2ee8-4938-b3bb-38f51b823875-4.gif")
            else:
                embed.set_thumbnail(url=user.avatar_url)
        if user.id == self.bot.user.id:
            embed = discord.Embed(title = f'Привет, я {user.name}', description=f"Тег: <@{user.id}>", color = 0x209af8)
            embed.add_field(name = "Владелец", value="<@390567552830406656>")
            embed.add_field(name = "Сервер бота", value = "Rebox Shit Force")
            embed.add_field(name = "Создан", value = f"<t:{ceil(time.mktime(datetime.datetime.strptime(str(user.created_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S').timetuple()))}:f>")
            embed.add_field(name = "На сервере с", value = f"<t:{ceil(time.mktime(datetime.datetime.strptime(str(user.joined_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S').timetuple()))}:f>")
            embed.add_field(name = "Сообщений", value = quantity)
            embed.add_field(name = "Статус", value = status)
            embed.add_field(name = "ОС", value = sys.platform)
            embed.add_field(name = "Версия Python", value = platform.python_version())
            embed.add_field(name = "Приглашение", value = "[Тык](https://discord.com/oauth2/authorize?client_id=935560968778448947&scope=bot&permissions=8)")
            embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Profile(bot))