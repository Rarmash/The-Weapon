from datetime import timedelta
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import servers_data

class Mod(commands.Cog):
    def __init__(self, client, servers_data):
        self.client = client
        self.servers_data = servers_data
    
    mod = SlashCommandGroup("mod", "Команды модерации")
    
    @mod.command(description='Забанить аутягу')
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        server_data = self.servers_data.get(str(ctx.guild.id))
        if not server_data:
            return
        embed = discord.Embed(
            description=f'<@{member.id}>, пошёл нахуй из интернета.\n**Бан по причине**: {reason}.',
            color=int(server_data.get("accent_color"), 16)
        )
        try:
            await member.send(embed=embed)
        except:
            pass
        await member.ban(reason = f"{ctx.author.display_name}: {reason}")
        await ctx.respond(embed=embed)
        
    @mod.command(description='Забанить аутягу по ID')
    async def banid(self, ctx, identificator, *, reason):
        server_data = self.servers_data.get(str(ctx.guild.id))
        if not server_data:
            return
        member = await self.client.fetch_user(identificator)
        await ctx.guild.ban(member, reason = f"{ctx.author.display_name}: {reason}")
        embed = discord.Embed(
            description=f'<@{identificator}>, пошёл нахуй из интернета.\n**Бан по причине**: {reason}.',
            color=int(server_data.get("accent_color"), 16)
        )
        await ctx.respond(embed=embed)
    
    @mod.command(description='Кикнуть аутягу')
    async def kick(self, ctx, member: discord.Member, *, reason):
        server_data = self.servers_data.get(str(ctx.guild.id))
        if not server_data:
            return
        await member.kick(reason = f"{ctx.author}: {reason}")
        embed = discord.Embed(
            description=f'<@{member.id}>, пошёл нахуй из интернета.\n**Кик по причине**: {reason}.',
            color=int(server_data.get("accent_color"), 16)
        )
        await ctx.respond(embed=embed)
    
    @mod.command(description='Замьютить аутягу')
    async def timeout(self, ctx, member: discord.Member, days: discord.Option(int, max_value = 27, default = 0, required = False), hours: discord.Option(int, max_value = 23, default = 0, required = False), minutes: discord.Option(int, max_value = 59, default = 0, required = False), seconds: discord.Option(int, max_value = 59, default = 0, required = False), reason=None):
        server_data = self.servers_data.get(str(ctx.guild.id))
        if not server_data:
            return
        duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
        if duration.total_seconds() != 0:
            await member.timeout_for(duration, reason=f"{ctx.author}: {reason}")
            embed = discord.Embed(
                description=f"<@{member.id}> в тайм-ауте на {days} дней {hours} часов {minutes} минут {seconds} секунд.\nПричина: {reason}.",
                color=int(server_data.get("accent_color"), 16)
            )
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("Вы не можете отправить пользователя в тайм-аут без определения срока!", ephemeral = True)
    
def setup(bot):
    bot.add_cog(Mod(bot, servers_data))