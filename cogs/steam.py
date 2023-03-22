import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import accent_color
import requests
import json

class Steam(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    steam = SlashCommandGroup("steam", "Команды по Steam")

    @steam.command(description='Посмотреть статистику по игроку')
    async def price(self, 
                    ctx: discord.ApplicationContext, 
                    appid, 
                    countrycode: discord.Option(str, choices=['RU', 'US', 'TR', 'AR', 'DE', 'UA'])
                    ):
        try:
            steamurl = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc={countrycode}&l=ru"
            app = requests.get(steamurl).json()[appid][u"data"]
            with open('data.json', "w") as f:
                json.dump(app, f, indent=4)
            embed = discord.Embed(
                title=app[u"name"],
                description=app[u"short_description"],
                color=accent_color
            )
            embed.set_thumbnail(url=app[u"header_image"])
            embed.add_field(name="Дата выпуска", value=app[u"release_date"][u"date"])
            devstring = "".join(f"{developer}, " for developer in app[u"developers"])[:-2]
            embed.add_field(name="Разработчик", value=devstring)
            pubstring = "".join(f"{publisher}, " for publisher in app[u"publishers"])[:-2]
            embed.add_field(name="Издатель", value=pubstring)
            if app[u"is_free"] == True:
                embed.add_field(name="Стоимость", value="Бесплатно")
            else:
                if app[u"price_overview"][u"discount_percent"] != 0:
                    embed.add_field(name="Стоимость", value=f'{app[u"price_overview"][u"final_formatted"]} (-{app[u"price_overview"][u"discount_percent"]}%)')
                else:
                    embed.add_field(name="Стоимость", value=app[u"price_overview"][u"final_formatted"])
            embed.add_field(name="Страница в Steam", value=f"[Тык](https://store.steampowered.com/app/{appid}/)")
            embed.add_field(name="SteamDB", value=f"[Тык](https://steamdb.info/app/{appid}/)")
            await ctx.respond(embed=embed)
        except KeyError:
            await ctx.respond("Такой игры не существует!")
        
def setup(bot):
    bot.add_cog(Steam(bot))