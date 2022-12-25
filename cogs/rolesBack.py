import json
import discord
from discord.ext import commands
from options import mongodb_link, rolespath
import pymongo

myclient = pymongo.MongoClient(mongodb_link)
Collection = myclient["Messages"]["UserRoles"]

try:
    rolesCount = json.load(open(rolespath, 'r'))
except:
    with open(rolespath, 'w+') as newsave:
        newsave.write('{}')
    rolesCount = json.load(open(rolespath, 'r'))

class RolesBack(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            with open(rolespath, 'r') as file:
                rolesCount = json.load(file)
                author = str(member.id)
            roles = str(rolesCount[author]).split("-")
            for role in roles:
                try:
                    await member.add_roles(discord.utils.get(member.guild.roles, id=int(role)))
                except:
                    pass
        except KeyError:
            pass
        
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        a = [r.id for r in member.roles]
        s = ''
        for rol in a:
            s += str(rol)
            s += "-"
        s = s[:-1]
        with open(rolespath, 'r') as file:
            rolesCount = json.load(file)
            author = str(member.id)
        rolesCount[author] = s
        with open(rolespath, 'w') as update_file:
            json.dump(rolesCount, update_file, indent=4)
            Collection.delete_many({})
            if isinstance(rolesCount, list):
                Collection.insert_many(rolesCount)
            else:
                Collection.insert_one(rolesCount)
        
    
def setup(bot):
    bot.add_cog(RolesBack(bot))