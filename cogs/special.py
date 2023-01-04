import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import accent_color, eventspath, mongodb_link
from datetime import datetime
import json
import pymongo

myclient = pymongo.MongoClient(mongodb_link)
Collection = myclient["Server"]["Events"]

with open(eventspath, "r", encoding='utf8') as file:
    data = json.load(file)

serverEvents = []

for i in data:
    a = [data[i][u'title'], str(data[i][u'description']).replace("\\n", "\n"), data[i][u'icon'], data[i][u'date']]

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
            num = len(data)+1
            entry = {
                f"event{num}":{
                        "title": f"{str(title)[0].lower()}{str(title)[1:]}",
                        "description": description,
                        "icon": icon,
                        "date": date
                    }
            }
            data.update(entry)
            serverEvents = []
            for i in data:
                a = [data[i][u"title"], data[i][u"description"], data[i][u"icon"], data[i][u"date"]]
                serverEvents.append(a) 
            with open(eventspath, 'w', encoding='utf8') as update_file:
                json.dump(data, update_file, indent=4, ensure_ascii=False)
                Collection.delete_many({})
                if isinstance(data, list):
                    Collection.insert_many(data)
                else:
                    Collection.insert_one(data)
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
        
    
def setup(bot):
    bot.add_cog(Special(bot))