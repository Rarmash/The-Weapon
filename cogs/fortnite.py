import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import fortniteapi, myclient, servers_data
import json
import requests

def fortnite_api_requests(username):
    request_url = f"https://fortnite-api.com/v2/stats/br/v2?name={username}"
    
    return json.loads(requests.get(
        request_url,
        params={
            "displayName": username
        },
        headers={
            "Authorization": fortniteapi
        }
    ).content)["data"]

def fortnite_api_requests_error(username):
    request_url = f"https://fortnite-api.com/v2/stats/br/v2?name={username}"
    
    return json.loads(requests.get(
        request_url,
        params={
            "displayName": username
        },
        headers={
            "Authorization": fortniteapi
        }
    ).content)["status"]

def fortnite_api_map():
    request_url = "https://fortnite-api.com/v1/map"
    
    return json.loads(requests.get(
        request_url,
        headers={
            "Authorization": fortniteapi
        }
    ).content)["data"]["images"]["pois"]

class Fortnite(commands.Cog):
    def __init__(self, bot, servers_data):
        self.Bot = bot
        self.servers_data = servers_data

    fortnite = SlashCommandGroup("fortnite", "Команды по Fortnite")

    @fortnite.command(description='Посмотреть статистику по игроку')
    async def stats(self, ctx: discord.ApplicationContext, username = None):
        server_data = self.servers_data.get(str(ctx.guild.id))
        if not server_data:
            return
        Collection = myclient[f"{str(ctx.guild.id)}"]["Users"]
        await ctx.defer()
        existense = True
        if username is None:
            user = Collection.find_one({"_id": str(ctx.author.id)})
            try:
                username = user["fortnite"]
            except:
                await ctx.respond("Вы не привязали профиль Fortnite к учётной записи Discord. Сделайте это, используя команду `/fortnite connect <username>`!")
                existense = False
        if existense == True:
            try:
                f = fortnite_api_requests(username)
                embed = discord.Embed(title=f'Статистика игрока {f["account"]["name"]}', color=int(server_data.get("accent_color"), 16))
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
                try:
                    embed.add_field(name = "Владелец профиля", value=f"<@{Collection.find_one({'fortnite': username})['_id']}>")
                except TypeError:
                    pass
                await ctx.respond(embed = embed)
            except KeyError:
                status = fortnite_api_requests_error(username)
                if status == 403:
                    guide_files = [
                        discord.File('resources/fortnite/fortnitestatsguide1.png'),
                        discord.File('resources/fortnite/fortnitestatsguide2.png'),
                        discord.File('resources/fortnite/fortnitestatsguide3.png')
                    ]
                    await ctx.respond(f"❗ Данные игрока **{username}** скрыты (ошибка **{status}**).\nЕсли это ваш аккаунт, откройте статистику в настройках игры.", files=guide_files)
                elif status == 404:
                    await ctx.respond(f"❗ Игрок **{username}** не найден (ошибка **{status}**).")
                else:
                    await ctx.respond(f"❓ Возникла ошибка **{status}**...")
        
    @fortnite.command(description='Посмотреть карту')
    async def map(self, ctx: discord.ApplicationContext):
        server_data = self.servers_data.get(str(ctx.guild.id))
        if not server_data:
            return
        embed = discord.Embed(title='Карта Fortnite', color=int(server_data.get("accent_color"), 16))
        embed.set_image(url = fortnite_api_map())
        await ctx.respond(embed = embed)    
        
    @fortnite.command(description='Привязать профиль Fortnite к учётной записи Discord')
    async def connect(self, ctx: discord.ApplicationContext, username):
        server_data = self.servers_data.get(str(ctx.guild.id))
        if not server_data:
            return
        Collection = myclient[f"{str(ctx.guild.id)}"]["Users"]
        await ctx.defer()
        author = str(ctx.author.id)
        try:
            f = fortnite_api_requests(username)
            Collection.update_one({"_id": author}, {"$set": {"fortnite": username}})
            embed = discord.Embed(description=f"Аккаунт {username} был успешно привязан к вашей учётной записи!\nЕсли вы измените никнейм в игре, не забудьте его перепривязать здесь.", color=int(server_data.get("accent_color"), 16))
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"При добавлении возникла ошибка {e}.\nВозможно, вы неверно указали никнейм.")
    
def setup(bot):
    bot.add_cog(Fortnite(bot, servers_data))