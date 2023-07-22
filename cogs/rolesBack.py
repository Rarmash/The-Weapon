import discord
from discord.ext import commands
from options import myclient

class RolesBack(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        author = str(member.id)
        server_id = str(member.guild.id)
        roles_collection = myclient[f"{server_id}"]["UserRoles"]
        roles = roles_collection.find_one({"_id": author})
        if roles:
            roles = roles["roles"].split("-")
            for role in roles:
                try:
                    await member.add_roles(discord.utils.get(member.guild.roles, id=int(role)))
                except:
                    pass
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        a = [r.id for r in member.roles]
        s = ''
        for rol in a:
            s += str(rol)
            s += "-"
        s = s[:-1]
        author = str(member.id)
        server_id = str(member.guild.id)
        roles_collection = myclient[f"{server_id}"]["UserRoles"]
        roles_collection.update_one({"_id": author}, {"$set": {"roles": s}}, upsert=True)
        
def setup(bot):
    bot.add_cog(RolesBack(bot))