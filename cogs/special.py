import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import accent_color, eventspath
from datetime import datetime
import json

with open(eventspath, "r", encoding='utf8') as file:
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
        k = 0
        for i in serverEvents:
            event1 = str(i[3]).split(" - ")
            if datetime.strptime(event1[0], '%d.%m.%Y %H:%M') < now < datetime.strptime(event1[1], '%d.%m.%Y %H:%M'):
                eventEmbed = discord.Embed(
                    title=f"Текущее событие: {i[0]}",
                    description=i[1],
                    color = accent_color
                )
                eventEmbed.set_thumbnail(url=i[2])
                eventEmbed.add_field(name="Событие закончится", value=f"<t:{str(datetime.strptime(event1[1], '%d.%m.%Y %H:%M').timestamp())[:-2]}:R>")
                k = 1
                break
        if k == 0:
            eventEmbed = discord.Embed(
                description="Сейчас на сервере не проходит никакое событие!",
                color = accent_color
            )
        await ctx.respond(embed = eventEmbed)
        
    @commands.slash_command(description='Добавить эвент в бота')
    async def addevent(self, ctx: discord.ApplicationContext, title, description, icon, date):
        try:
            num = len(data)+1
            entry = {
                f"event{num}": [
                    {
                        "title": f"{str(title)[0].lower()}{str(title)[1:]}",
                        "description": description,
                        "icon": icon,
                        "date": date
                    }
                ]
            }
            data.update(entry)
            with open(eventspath, "w", encoding='utf8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            serverEvents = []
            for i in data:
                a = [data[i][0][u'title'], data[i][0][u'description'], data[i][0][u'icon'], data[i][0][u'date']]
                serverEvents.append(a)
            event1 = str(serverEvents[num-1][3]).split(" - ")
            eventEmbed = discord.Embed(
                    title=f"Добавленное событие: {serverEvents[num-1][0]}",
                    description=serverEvents[num-1][1],
                    color = accent_color
                )
            eventEmbed.set_thumbnail(url=serverEvents[num-1][2])
            eventEmbed.add_field(name="Событие начнётся", value=f"<t:{str(datetime.strptime(event1[0], '%d.%m.%Y %H:%M').timestamp())[:-2]}:R>")
            eventEmbed.add_field(name="Событие закончится", value=f"<t:{str(datetime.strptime(event1[1], '%d.%m.%Y %H:%M').timestamp())[:-2]}:R>")
            await ctx.respond(embed = eventEmbed)
        except Exception as e:
            await ctx.respond(f"Всё хуйня, давай по новой ({e})")
        
    
def setup(bot):
    bot.add_cog(Special(bot))