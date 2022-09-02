import json
import discord
from discord.ext import commands
import time
import datetime
from math import ceil
import sys
import platform
from options import insider_id, datapath, admin_id, accent_color, timeoutpath

class Profile(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    @commands.slash_command(description='Посмотреть карточку профиля')
    async def profile(self, ctx: discord.ApplicationContext, user: discord.Member = None):
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
        with open(datapath) as json_file:
            json_data = json.load(json_file)
        with open(timeoutpath) as json_file:
            timeout_data = json.load(json_file)
        for users in json_data:
            if int(users) == user.id:
                quantity = json_data[users]
        try:
            quantity
        except:
            quantity = 0
        for users in timeout_data:
            if int(users) == user.id:
                timeoutquantity = timeout_data[users]
        try:
            timeoutquantity
        except:
            timeoutquantity = 0
        if user.id != self.Bot.user.id:
            time_out = '(в тайм-ауте)' if user.timed_out else ''
            embed = discord.Embed(title = f'Привет, я {user.name}', description=f"<@{user.id}> — {status} {time_out}", color = accent_color)
            embed.add_field(name = "Регистрация", value = f"<t:{ceil(time.mktime(datetime.datetime.strptime(str(user.created_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S').timetuple()))}:f>")
            embed.add_field(name = "На сервере с", value = f"<t:{ceil(time.mktime(datetime.datetime.strptime(str(user.joined_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S').timetuple()))}:f>")
            if not user.bot:
                embed.add_field(name = "Сообщений", value = quantity)
                embed.add_field(name = "Всего тайм-аутов", value = timeoutquantity)
            if discord.utils.get(ctx.guild.roles, id=insider_id) in user.roles:
                embed.set_footer(text="Принимает участие в тестировании и помогает серверу стать лучше")
            embed.set_thumbnail(url=user.avatar)
        if user.id == self.Bot.user.id:
            embed = discord.Embed(title = f'Привет, я {user.name}', description=f"Тег: <@{user.id}>", color = accent_color)
            embed.add_field(name = "Владелец", value=f"<@{admin_id}>")
            embed.add_field(name = "Сервер бота", value = "Rebox Shit Force")
            embed.add_field(name = "Создан", value = f"<t:{ceil(time.mktime(datetime.datetime.strptime(str(user.created_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S').timetuple()))}:f>")
            embed.add_field(name = "На сервере с", value = f"<t:{ceil(time.mktime(datetime.datetime.strptime(str(user.joined_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S').timetuple()))}:f>")
            embed.add_field(name = "Статус", value = status)
            embed.add_field(name = "ОС", value = sys.platform)
            embed.add_field(name = "Версия Python", value = platform.python_version())
            embed.add_field(name = "Версия Pycord", value = discord.__version__)
            embed.add_field(name = "Приглашение", value = "[Тык](https://discord.com/oauth2/authorize?client_id=935560968778448947&scope=bot&permissions=8)")
            embed.set_thumbnail(url=user.avatar)
        await ctx.respond(embed = embed)

def setup(bot):
    bot.add_cog(Profile(bot))