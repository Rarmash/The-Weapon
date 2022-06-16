import discord
from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MemberNotFound):
            await ctx.message.delete()
            embed = discord.Embed(description="❌ Пользователь не найден", color = 0xff0000)
            await ctx.send(embed=embed, delete_after=5.0)

def setup(bot):
    bot.add_cog(Events(bot))