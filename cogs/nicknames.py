from discord.ext import commands

symbols = ['ٴ']
PLACEHOLDER_NICKNAME = 'По правилу 7 я пидор'

class Nicknames(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot
    
    @commands.Cog.listener()
    async def on_member_update(self, memberBefore, memberAfter):
        for symbol in symbols:
            if symbol in memberAfter.display_name:
                await memberAfter.edit(nick=PLACEHOLDER_NICKNAME)
                break

    # triggered on username change
    @commands.Cog.listener()
    async def on_user_update(self, memberBefore, memberAfter):
        for symbol in symbols:
            if symbol in memberAfter.display_name:
                await memberAfter.edit(nick=PLACEHOLDER_NICKNAME)
                break


    # check if new members' usernames need filtering
    @commands.Cog.listener()
    async def on_member_join(self, member):
        for symbol in symbols:
            if symbol in member.display_name:
                await member.edit(nick=PLACEHOLDER_NICKNAME)
                break
    
def setup(bot):
    bot.add_cog(Nicknames(bot))