import discord
from discord.ext import commands
from options import accent_color
from datetime import datetime
import json

with open("serverEvents.json", "r", encoding='utf8') as file:
    data = json.load(file)

serverEvents = []

for i in data:
    a = [data[i][0][u'title'], data[i][0][u'description'], data[i][0][u'icon'], data[i][0][u'date']]

    serverEvents.append(a)

class Special(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot
    
    @commands.slash_command(description='Текущий эвент на сервере')
    async def event(self, ctx: discord.ApplicationContext):
        now = datetime.now()
        event1 = str(serverEvents[0][3]).split(" - ")
        if datetime.strptime(event1[0], '%d.%m.%Y %H:%M') < now < datetime.strptime(event1[1], '%d.%m.%Y %H:%M'):
            eventEmbed = discord.Embed(
                title=f"Текущее событие: {serverEvents[0][0]}",
                description=serverEvents[0][1],
                color = accent_color
            )
            eventEmbed.set_thumbnail(url=serverEvents[0][2])
            eventEmbed.add_field(name="Событие закончится", value=f"<t:{str(datetime.strptime(event1[1], '%d.%m.%Y %H:%M').timestamp())[:-2]}:R>")
        else:
            eventEmbed = discord.Embed(
                description="Сейчас на сервере не проходит никакое событие!",
                color = accent_color
            )
        await ctx.respond(embed = eventEmbed)
        
    
def setup(bot):
    bot.add_cog(Special(bot))