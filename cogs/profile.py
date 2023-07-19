import discord
from discord.ext import commands
import time
import datetime
from math import ceil
import sys
import platform
from options import insider_id, admin_id, accent_color, Collection, version

class Profile(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    @commands.slash_command(description='Посмотреть карточку профиля')
    async def profile(self, ctx: discord.ApplicationContext, user: discord.Member = None):
        date_format = "%#d.%#m.%Y в %H:%M:%S"
        if user is None:
            user = ctx.author
        status = self.get_status_emoji(user.status)
        user_data = Collection.find_one({"_id": str(user.id)})
        if user.id != self.Bot.user.id:
            time_out = '(в тайм-ауте)' if user.timed_out else ''
            embed = discord.Embed(title = f'Привет, я {user.name}', description=f"<@{user.id}> — {status} {time_out}", color = accent_color)
            embed.add_field(name = "Регистрация", value = f"<t:{ceil(time.mktime((datetime.datetime.strptime(str(user.created_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S')+datetime.timedelta(hours=3)).timetuple()))}:f>")
            embed.add_field(name = "На сервере с", value = f"<t:{ceil(time.mktime((datetime.datetime.strptime(str(user.joined_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S')+datetime.timedelta(hours=3)).timetuple()))}:f>")
            if not user.bot:
                embed.add_field(name = "Сообщений", value = user_data['messages'])
                embed.add_field(name = "Всего тайм-аутов", value = user_data['timeouts'])
                if "xbox" in user_data:
                    embed.add_field(name = "Профиль Xbox", value = f"[{user_data['xbox']}](https://account.xbox.com/ru-ru/Profile?Gamertag={str(user_data['xbox']).replace(' ', '%20')})")
                if "fortnite" in user_data:
                    embed.add_field(name = "Профиль Fortnite", value = user_data['fortnite'])
            if discord.utils.get(ctx.guild.roles, id=insider_id) in user.roles:
                embed.set_footer(text="Принимает участие в тестировании и помогает серверу стать лучше")
            embed.set_thumbnail(url=user.avatar)
        if user.id == self.Bot.user.id:
            embed = discord.Embed(title = f'Привет, я {user.name}', description=f"Тег: <@{user.id}>", color = accent_color)
            embed.add_field(name = "Владелец", value=f"<@{admin_id}>")
            embed.add_field(name = "Сервер бота", value = "Rebox Shit Force")
            embed.add_field(name = "Создан", value = f"<t:{ceil(time.mktime((datetime.datetime.strptime(str(user.created_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S')+datetime.timedelta(hours=3)).timetuple()))}:f>")
            embed.add_field(name = "На сервере с", value = f"<t:{ceil(time.mktime((datetime.datetime.strptime(str(user.joined_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S')+datetime.timedelta(hours=3)).timetuple()))}:f>")
            embed.add_field(name = "Статус", value = status)
            embed.add_field(name = "ОС", value = sys.platform)
            embed.add_field(name = "Версия бота", value = version)
            embed.add_field(name = "Версия Python", value = platform.python_version())
            embed.add_field(name = "Версия Pycord", value = discord.__version__)
            embed.add_field(name = "Приглашение", value = "[Тык](https://discord.com/oauth2/authorize?client_id=935560968778448947&scope=bot&permissions=8)")
            embed.set_thumbnail(url=user.avatar)
        await ctx.respond(embed = embed)
        
    def get_status_emoji(self, status):
        if status == discord.Status.online:
            return "🟢 в сети"
        elif status == discord.Status.offline:
            return "⚪ не в сети"
        elif status == discord.Status.idle:
            return "🌙 не активен"
        elif status == discord.Status.dnd:
            return "⛔ не беспокоить"

def setup(bot):
    bot.add_cog(Profile(bot))