import discord
from discord.ext import commands
from bannedChannels import bannedChannels
from bannedUsers import bannedUsers
from options import log_channel as logger
from options import mongodb_link
import pymongo
import json

bmbk = 398913828781424661
bmbklog = 1000535903128780860

class Bambook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        channel = self.bot.get_channel(bmbklog)
        if ctx.author.id == bmbk:
            embed = discord.Embed(
                title='Удалённое сообщение',
                description=ctx.content,
                color=0x209af8
            )
            embed.add_field(
                name='Автор',
                value=f'<@{ctx.author.id}>'
            )
            embed.add_field(
                name='Канал',
                value=f'<#{ctx.channel.id}>'
            )
            await channel.send(embed=embed)
            await ctx.delete()

    @commands.Cog.listener()
    async def on_user_update(self, memberBefore, memberAfter):
        if memberAfter.author.id == bmbk:
            await memberAfter.edit(nick='оп')
            
    @commands.Cog.listener()
    async def on_member_update(self, memberBefore, memberAfter):
        if memberAfter.author.id == bmbk:
            await memberAfter.edit(nick='оп')

def setup(bot):
    bot.add_cog(Bambook(bot))
