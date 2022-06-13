import discord
from discord.ext import commands

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, *, user: discord.Member = None):
        date_format = "%#d.%#m.%Y в %H:%M"
        if user is None:
            user = ctx.author
        embed = discord.Embed(title = f'Карточка {user.name}', description=f"Тег: <@{user.id}>", color = 0x209af8)
        embed.add_field(name = "Регистрация", value = user.created_at.strftime(date_format))
        embed.add_field(name = "На сервере с", value = user.joined_at.strftime(date_format))
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Profile(bot))