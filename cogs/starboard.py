import discord
from discord.ext import commands
from options import media_channel
from discord.utils import get

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == media_channel and payload.emoji.name == "📌":
            channel = await self.Bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            reaction = get(message.reactions, emoji=payload.emoji.name)
            if reaction and reaction.count >= 10:
                await message.pin()
        
def setup(bot):
    bot.add_cog(Starboard(bot))