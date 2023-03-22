import discord
from discord.ext import commands
from options import accent_color, EventsCollection
from datetime import datetime

class Special(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot
    
    @commands.slash_command(description='Текущий эвент на сервере')
    async def event(self, ctx: discord.ApplicationContext):
        now = datetime.now()
        k = 0
        serverEvents = []
        for event in EventsCollection.find():
            a = [event["title"], event["description"], event["icon"], event["date"]]
            serverEvents.append(a)
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
            num = EventsCollection.count_documents({})+1
            entry = {
                    "title": f"{str(title)[0].lower()}{str(title)[1:]}",
                    "description": description,
                    "icon": icon,
                    "date": date
            }
            EventsCollection.insert_one(entry)
            serverEvents = []
            for event in EventsCollection.find():
                a = [event["title"], event["description"], event["icon"], event["date"]]
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
    
def setup(bot):
    bot.add_cog(Special(bot))