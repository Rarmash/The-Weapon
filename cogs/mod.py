from discord import Option
from datetime import timedelta
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import accent_color
import datetime

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    mod = SlashCommandGroup("mod", "Команды модерации")
    
    @mod.command(description='Забанить аутягу')
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        await member.ban(reason = f"{ctx.author}: {reason}")
        embed = discord.Embed(
            description=f'<@{member.id}>, пошёл нахуй из интернета.\n**Бан по причине**: {reason}.',
            color=accent_color
        )
        await ctx.respond(embed=embed)
    
    @mod.command(description='Кикнуть аутягу')
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason = f"{ctx.author}: {reason}")
        embed = discord.Embed(
            description=f'<@{member.id}>, пошёл нахуй из интернета.\n**Кик по причине**: {reason}.',
            color=accent_color
        )
        await ctx.respond(embed=embed)
    
    @mod.command(description='Замьютить аутягу')
    async def timeout(self, ctx, member: discord.Member, days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, max_value = 23, default = 0, required = False), minutes: Option(int, max_value = 59, default = 0, required = False), seconds: Option(int, max_value = 59, default = 0, required = False), reason=None):
        duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
        if days == 0 and hours == 0 and minutes == 0 and seconds == 0:
            await ctx.respond("Вы не можете отправить пользователя в тайм-аут без определения срока!", ephemeral = True)
        else:
            await member.timeout_for(duration, reason=f"{ctx.author}: {reason}")
            embed = discord.Embed(
                description=f"<@{member.id}> в тайм-ауте на {days} дней {hours} часов {minutes} минут {seconds} секунд.\nПричина: {reason}.",
                color=accent_color
            )
            await ctx.respond(embed=embed)
    
def setup(bot):
    bot.add_cog(Mod(bot))