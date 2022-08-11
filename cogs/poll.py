import discord
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 931963318262968412:
            channel = await self.Bot.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            # iterating through each reaction in the message
            for r in message.reactions:

                # checks the reactant isn't a bot and the emoji isn't the one they just reacted with
                if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):

                    # removes the reaction
                    await message.remove_reaction(r.emoji, payload.member)
    
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