import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.slash_command(description='Забанить аутягу')
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        await member.ban(reason = reason)
        embed = discord.Embed(
            description=f'<@{member.id}>, пошёл нахуй из интернета.\n**Бан по причине**: {reason}.',
            color=0x209af8
        )
        await ctx.respond(embed=embed)
    
def setup(bot):
    bot.add_cog(Mod(bot))