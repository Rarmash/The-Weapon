import discord
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, *, question=None):
        if question is None:
            await ctx.message.delete()
            await ctx.send("Пожалуйста, укажите ваше предложение!", delete_after=5.0)
        else:
            pollEmbed = discord.Embed(title = "Новое предложение", description = f"{question}", color = 0x209af8)
            pollEmbed.add_field(
                name = 'Автор',
                value = f'<@{ctx.author.id}>'
            )
            await ctx.message.delete()
            poll_msg = await ctx.send(embed = pollEmbed)

            await poll_msg.add_reaction("<:MinecraftAccept:936636758135828502>")
            await poll_msg.add_reaction("<:MinecraftDeny:936636758127439883>")


def setup(bot):
    bot.add_cog(Poll(bot))