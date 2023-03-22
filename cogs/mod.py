from datetime import timedelta
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import accent_color

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    mod = SlashCommandGroup("mod", "Команды модерации")
    
    @mod.command(description='Забанить аутягу')
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        embed = discord.Embed(
            description=f'<@{member.id}>, пошёл нахуй из интернета.\n**Бан по причине**: {reason}.',
            color=accent_color
        )
        try:
            await member.send(embed=embed)
        except:
            pass
        await member.ban(reason = f"{ctx.author}: {reason}")
        await ctx.respond(embed=embed)
        
    @mod.command(description='Забанить аутягу по ID')
    async def banid(self, ctx, identificator, *, reason = None):
        member = await self.client.fetch_user(identificator)
        await ctx.guild.ban(member, reason = f"{ctx.author}: {reason}")
        embed = discord.Embed(
            description=f'<@{identificator}>, пошёл нахуй из интернета.\n**Бан по причине**: {reason}.',
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
    async def timeout(self, ctx, member: discord.Member, days: discord.Option(int, max_value = 27, default = 0, required = False), hours: discord.Option(int, max_value = 23, default = 0, required = False), minutes: discord.Option(int, max_value = 59, default = 0, required = False), seconds: discord.Option(int, max_value = 59, default = 0, required = False), reason=None):
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
        
    @mod.command(description='Снести человеку никнейм')
    async def bannickname(self, ctx, member: discord.Member, reason: discord.Option(int, max_value = 11)):
        PLACEHOLDER_NICKNAME = f'Правило {reason}: исправь ник'
        embed = discord.Embed(description=f"Никнейм пользователя {member.display_name} был изменён по правилу {reason}.", color=accent_color)
        await ctx.respond(embed = embed)
        await member.edit(nick=PLACEHOLDER_NICKNAME)  
    
def setup(bot):
    bot.add_cog(Mod(bot))