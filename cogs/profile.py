import discord
from discord.ext import commands

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        date_format = "%#d.%#m.%Y в %H:%M"
        if user is None:
            user = ctx.author
        if user.id != self.bot.user.id:
            if user.status == discord.Status.online:
                status = "В сети"
            if user.status == discord.Status.offline:
                status = "⚪ Не в сети"
            if user.status == discord.Status.idle:
                status = "Не активен"
            if user.status == discord.Status.dnd:
                status = "Не беспокоить"
            embed = discord.Embed(title = f'Карточка {user.name}', description=f"Тег: <@{user.id}>", color = 0x209af8)
            embed.add_field(name = "Регистрация", value = user.created_at.strftime(date_format))
            embed.add_field(name = "На сервере с", value = user.joined_at.strftime(date_format))
            #embed.add_field(name = "Статус", value = user.status)
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed = embed)
        if user.id == self.bot.user.id:
            if user.status == discord.Status.online:
                status = "В сети"
            if user.status == discord.Status.offline:
                status = "⚪ Не в сети"
            if user.status == discord.Status.idle:
                status = "Не активен"
            if user.status == discord.Status.dnd:
                status = "Не беспокоить"
            embed = discord.Embed(title = f'Карточка {user.name}', description=f"Тег: <@{user.id}>", color = 0x209af8)
            embed.add_field(name = "Владелец", value = f"<@390567552830406656>")
            embed.add_field(name = "Сервер бота", value = "Rebox Shit Force")
            embed.add_field(name = "Создан", value = user.created_at.strftime(date_format))
            embed.add_field(name = "На сервере с", value = user.joined_at.strftime(date_format))
            embed.add_field(name = "Статус", value = status)
            embed.add_field(name = "Приглашение", value = "[Тык](https://discord.com/oauth2/authorize?client_id=935560968778448947&scope=bot&permissions=8)")
            embed.set_thumbnail(url=user.avatar_url)
            await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Profile(bot))