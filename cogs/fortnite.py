import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import accent_color, fortniteapi
import json
import requests

def fortnite_api_requests(username):
    request_url = f"https://fortnite-api.com/v2/stats/br/v2?name={username}"
    
    return json.loads(requests.get(
        request_url,
        params={
            "displayName": username,
            "platform": "epic"
        },
        headers={
            "Authorization": fortniteapi
        }
    ).content)["data"]

def fortnite_api_map():
    request_url = "https://fortnite-api.com/v1/map"
    
    return json.loads(requests.get(
        request_url,
        headers={
            "Authorization": fortniteapi
        }
    ).content)["data"]["images"]["pois"]

class Fortnite(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    fortnite = SlashCommandGroup("fortnite", "Команды по Fortnite")

    @fortnite.command(description='Посмотреть статистику по игроку')
    async def stats(self, ctx: discord.ApplicationContext, username):
        try:
            f = fortnite_api_requests(username)
            embed = discord.Embed(title=f'Статистика игрока {f["account"]["name"]}', color=accent_color)
            embed.add_field(name="🎟️ Уровень боевого пропуска", value=f'{f["battlePass"]["level"]}')
            embed.add_field(name="🎮 Всего матчей сыграно", value=f'{f["stats"]["all"]["overall"]["matches"]}')
            embed.add_field(name="👑 Всего побед", value=f'{f["stats"]["all"]["overall"]["wins"]}')
            embed.add_field(name="🎖 Всего топ-3", value=f'{f["stats"]["all"]["overall"]["top3"]}')
            embed.add_field(name="🎖 Всего топ-5", value=f'{f["stats"]["all"]["overall"]["top5"]}')
            embed.add_field(name="🎖 Всего топ-10", value=f'{f["stats"]["all"]["overall"]["top10"]}')
            embed.add_field(name="🎖 Всего топ-25", value=f'{f["stats"]["all"]["overall"]["top25"]}')
            embed.add_field(name="💀 Всего убийств", value=f'{f["stats"]["all"]["overall"]["kills"]}')
            embed.add_field(name="☠️ Убийств в минуту", value=f'{f["stats"]["all"]["overall"]["killsPerMin"]}')
            embed.add_field(name="☠️ Убийств за матч", value=f'{f["stats"]["all"]["overall"]["killsPerMatch"]}')
            embed.add_field(name="⚰️ Всего смертей", value=f'{f["stats"]["all"]["overall"]["deaths"]}')
            embed.add_field(name="📈 Общее K/D", value=f'{f["stats"]["all"]["overall"]["kd"]}')
            embed.add_field(name="📉 % побед", value=f'{f["stats"]["all"]["overall"]["winRate"]}')
            embed.add_field(name="🕓 Всего сыграно минут", value=f'{f["stats"]["all"]["overall"]["minutesPlayed"]}')
            embed.add_field(name="🙋‍♂️ Всего игроков пережито", value=f'{f["stats"]["all"]["overall"]["playersOutlived"]}')
            await ctx.respond(embed = embed)
        except:
            await ctx.respond('📛 Игрок не найден!')
        
    @fortnite.command(description='Посмотреть карту')
    async def map(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title='Карта Fortnite', color=accent_color)
        embed.set_image(url = fortnite_api_map())
        await ctx.respond(embed = embed)    
    
def setup(bot):
    bot.add_cog(Fortnite(bot))