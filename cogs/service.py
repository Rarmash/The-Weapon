import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import admin_id
import os
from options import token, mongodb_link, userpath
import time
import datetime
from math import ceil
class Service(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    service = SlashCommandGroup("service", "Сервисные команды")
    
    @commands.slash_command(description='Посмотреть карточку сервера')
    async def server(self, ctx):
        guild = ctx.guild
        date_format = "%#d.%#m.%Y в %H:%M:%S"
        embed = discord.Embed(title=f"Информация о сервере {guild}", color = 0x209af8)
        embed.set_thumbnail(url=guild.icon)
        embed.add_field(name="Описание", value=guild.description)
        embed.add_field(name="Каналов", value=len(guild.channels))
        embed.add_field(name="Ролей", value=len(guild.roles))
        embed.add_field(name="Бустеров", value=len(guild.premium_subscribers))
        embed.add_field(name="Участников", value=guild.member_count-len(([member for member in ctx.guild.members if member.bot])))
        embed.add_field(name="Ботов", value=len(([member for member in ctx.guild.members if member.bot])))
        embed.add_field(name="Создан", value=f"<t:{ceil(time.mktime(datetime.datetime.strptime(str(guild.created_at.strftime(date_format)), '%d.%m.%Y в %H:%M:%S').timetuple()))}:f>")
        embed.add_field(name="Владелец", value=f"<@{guild.owner.id}>")
        await ctx.respond(embed=embed)   
    
    @service.command(description='Проверить пинг')
    async def ping(self, ctx):
        await ctx.respond(f"Понг! :ping_pong: Задержка: {self.bot.latency*1000:,.0f} ms.")
    
    @commands.slash_command(description='Pat Eufeek')
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def pateufeek(self, ctx):
        await ctx.respond("https://cdn.discordapp.com/attachments/646322883555098647/1077840268667146241/5e7f7340-669c-4b2a-9c9f-9cb82a6f2943.gif")
        
    @service.command(description='Отправить JSON всех участников')
    async def jsondump(self, ctx):
        await ctx.respond('Дамп JSON файла всех участников.', file=discord.File(userpath))
        
    @service.command(description='Отправить инфу по боту')
    async def botsecret(self, ctx):
        if ctx.author.id == admin_id:
            await ctx.respond("Скинул в ЛС.")
            await ctx.author.send(f'Токен бота: `{token}`\nБаза MongoDB: `{mongodb_link}`')
        else:
            await ctx.respond("Недостаточно прав для выполнения данной команды.")   

    @service.command(description='Выключить бота')
    async def shutdown(self, ctx):
        if ctx.author.id == admin_id:
            await ctx.respond("Завершение работы... :wave:")
            os.abort()
        else:
            await ctx.respond("Недостаточно прав для выполнения данной команды.")
            
    @service.command()
    async def unload(self, ctx, extension):
        if ctx.author.id == admin_id:
            self.bot.unload_extension(f"cogs.{extension}")
            await ctx.respond(f"**cogs.{extension}** выгружается...")
        else:
            await ctx.respond("Недостаточно прав для выполнения данной команды.")

    @service.command()
    async def load(self, ctx, extension):
        if ctx.author.id == admin_id:
            self.bot.load_extension(f"cogs.{extension}")
            await ctx.respond(f"**cogs.{extension}** запускается...")
        else:
            await ctx.respond("Недостаточно прав для выполнения данной команды.")

    @service.command()
    async def reload(self, ctx, extension):
        if ctx.author.id == admin_id:
            self.bot.unload_extension(f"cogs.{extension}")
            self.bot.load_extension(f"cogs.{extension}")
            await ctx.respond(f"**cogs.{extension}** перезапускается...")
        else:
            await ctx.respond("Недостаточно прав для выполнения данной команды.")

def setup(bot):
    bot.add_cog(Service(bot))