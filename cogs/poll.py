import discord
from discord.ext import commands
from options import poll_channel, accent_color

class Poll(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == poll_channel:
            channel = await self.Bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            for r in message.reactions:
                if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):
                    await message.remove_reaction(r.emoji, payload.member)
    
    @commands.slash_command(description='Предложить идею')
    async def poll(self, ctx: discord.ApplicationContext, *, question):
        pollEmbed = discord.Embed(title = "Новое предложение", description = f"{question}", color = accent_color)
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