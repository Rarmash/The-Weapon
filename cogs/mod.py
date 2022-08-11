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
        await member.ban(reason = reason)
        embed = discord.Embed(
            description=f'<@{member.id}>, пошёл нахуй из интернета.\n**Бан по причине**: {reason}.',
            color=accent_color
        )
        await ctx.respond(embed=embed)
    
    @mod.command(description='Кикнуть аутягу')
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason = reason)
        embed = discord.Embed(
            description=f'<@{member.id}>, пошёл нахуй из интернета.\n**Кик по причине**: {reason}.',
            color=accent_color
        )
        await ctx.respond(embed=embed)
    
def setup(bot):
    bot.add_cog(Mod(bot))