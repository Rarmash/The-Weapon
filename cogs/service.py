import discord
from discord.ext import commands
from options import admin_id as administrator
import os
from options import token, mongodb_link
class Service(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(description='Посмотреть карточку сервера')
    async def server(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Информация о сервере {guild}", color = 0x209af8)
        embed.set_thumbnail(url=guild.icon)
        embed.add_field(name="Описание", value=guild.description)
        embed.add_field(name="Каналов", value=len(guild.channels))
        embed.add_field(name="Ролей", value=len(guild.roles))
        embed.add_field(name="Бустеров", value=len(guild.premium_subscribers))
        embed.add_field(name="Участников", value=guild.member_count)
        embed.add_field(name="Создан", value=str(guild.created_at)[:-7])
        embed.add_field(name="Владелец", value=guild.owner)
        await ctx.respond(embed=embed)   
    
    @commands.slash_command(description='Проверить пинг')
    async def ping(self, ctx):
        await ctx.respond(f"Понг! :ping_pong: Задержка: {self.bot.latency*1000:,.0f} ms.")
    
    @commands.slash_command(description='Посмотреть аватарку')
    async def avatar(self, ctx):
        author = ctx.author
        
        embed = discord.Embed(title=f"Аватарка {author}"[:-5],
                                color=discord.Color.dark_gray())
        link = author.avatar
        embed.set_image(url = link)

        await ctx.respond(embed=embed)
    
    @commands.slash_command(description='Pat Eufeek')
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def pateufeek(self, ctx):
        await ctx.respond("https://media.discordapp.net/attachments/964614960325992478/982716016184410122/4c8de376-2ee8-4938-b3bb-38f51b823875-4.gif")


    @commands.slash_command(description='И тебе привет')
    async def hello(self, ctx):
        author = ctx.author
        await ctx.respond(f'Привет, {author.mention}!')
        
    @commands.slash_command(description='Сказать сообщение')
    async def say(self, ctx, msg):
        await ctx.send(msg)
        
    @commands.slash_command(description='Отправить JSON всех участников')
    async def jsondump(self, ctx):
        await ctx.respond('Дамп JSON файла всех участников.', file=discord.File('data.json'))
        
    @commands.slash_command(description='Отправить инфу по боту')
    async def botsecret(self, ctx):
        if ctx.author.id == administrator:
            await ctx.respond("Скинул в ЛС.")
            await ctx.author.send(f'Токен бота: `{token}`\nБаза MongoDB: `{mongodb_link}`')
        else:
            await ctx.respond("Недостаточно прав для выполнения данной команды.")   
        
    @commands.slash_command(description='Выключить бота')
    async def shutdown(self, ctx):
        if ctx.author.id == administrator:
            await ctx.respond("Завершение работы... :wave:")
            os.abort()
        else:
            await ctx.respond("Недостаточно прав для выполнения данной команды.")

def setup(bot):
    bot.add_cog(Service(bot))