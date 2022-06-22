import discord
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description='Предложить идею')
    async def poll(self, ctx: discord.ApplicationContext, *, question):
        pollEmbed = discord.Embed(title = "Новое предложение", description = f"{question}", color = 0x209af8)
        pollEmbed.add_field(
            name = 'Автор',
            value = f'<@{ctx.author.id}>'
        )
        
        poll_msg = await ctx.respond(embed = pollEmbed)
        poll_message = await poll_msg.original_message()
        await poll_message.add_reaction("<:MinecraftAccept:936636758135828502>")
        await poll_message.add_reaction("<:MinecraftDeny:936636758127439883>")
    
def setup(bot):
    bot.add_cog(Poll(bot))