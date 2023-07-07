import requests
import discord
import json
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import xboxapi, debugmode, Collection

def get_user_info(gamertag):
    response = requests.get(f'https://xbl.io/api/v2/search/{gamertag}', headers={'x-authorization': xboxapi})
    response = response.json()[u"people"][0]
    if debugmode == "ON":
        with open("response.json", 'w') as f:
            json.dump(response, f, indent=4)
    return response

def get_games_amount(xuid):
    response = requests.get(f'https://xbl.io/api/v2/achievements/player/{xuid}', headers={'x-authorization': xboxapi})
    response = response.json()
    if debugmode == "ON":
        with open("responsegames.json", 'w') as f:
            json.dump(response, f, indent=4)
    title_count = len(response["titles"])
    recentgame = response["titles"][0]["name"]
    curscoreonrecgame = response["titles"][0]["achievement"]["currentGamerscore"]
    totalscoreonrecgame = response["titles"][0]["achievement"]["totalGamerscore"]
    return title_count, recentgame, curscoreonrecgame, totalscoreonrecgame

class Xbox(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    xbox = SlashCommandGroup("xbox", "Команды Xbox")

    @xbox.command(description='Посмотреть статистику по пользователю')
    async def stats(self, ctx: discord.ApplicationContext, gamertag = None):
        await ctx.defer()
        existense = True
        if gamertag is None:
            user = Collection.find_one({"_id": str(ctx.author.id)})
            try:
                gamertag = user["xbox"]
            except:
                await ctx.respond("Вы не привязали профиль Xbox к учётной записи Discord. Сделайте это, используя команду `/xbox connect <Gamertag>`!")
                existense = False
        if existense == True:
            try:
                f = get_user_info(gamertag)
                embed = discord.Embed(title=f'Карточка игрока {f["gamertag"]}', color=int(f["preferredColor"]["primaryColor"], 16))
                embed.add_field(name="Gamerscore", value=f'🅖 {f["gamerScore"]}')
                if f["detail"]["accountTier"] == "Gold":
                    goldstatus = "Активен"
                else:
                    goldstatus = "Не активен"
                embed.add_field(name="Статус Gold", value=goldstatus)
                embed.add_field(name="Фолловеров", value=f'{f["detail"]["followerCount"]}')
                embed.add_field(name="Друзей", value=f'{f["detail"]["followingCount"]}')
                try:
                    title_count, recentgame, curscoreonrecgame, totalscoreonrecgame = get_games_amount(f["xuid"])
                    embed.add_field(name="Сыграно игр", value=title_count)
                    embed.add_field(name="Недавно играл в", value=f"{recentgame} (🅖 {curscoreonrecgame}/{totalscoreonrecgame})")
                except IndexError:
                    embed.add_field(name="Игровая статистика", value="Отсутствует, либо скрыта")
                embed.add_field(name = "Ссылка на профиль", value = f"[Тык](https://account.xbox.com/ru-ru/Profile?Gamertag={str(f['gamertag']).replace(' ', '%20')})")
                try:
                    embed.add_field(name = "Владелец профиля", value=f"<@{Collection.find_one({'xbox': gamertag})['_id']}>")
                except TypeError:
                    pass
                if f["isXbox360Gamerpic"] == True:
                    embed.set_thumbnail(url=f"http://avatar.xboxlive.com/avatar/{str(f['gamertag']).replace(' ', '%20')}/avatarpic-l.png")
                else:
                    embed.set_thumbnail(url=f["displayPicRaw"])
                await ctx.respond(embed = embed)
            except KeyError as e:
                await ctx.respond(f"❓ Возникла ошибка {e}...", ephemeral=True)

    @xbox.command(description='Привязать профиль Xbox к учётной записи Discord')
    async def connect(self, ctx: discord.ApplicationContext, gamertag):
        await ctx.defer()
        author = str(ctx.author.id)
        try:
            f = get_user_info(gamertag)
            Collection.update_one({"_id": author}, {"$set": {"xbox": gamertag}})
            embed = discord.Embed(description=f"Аккаунт {gamertag} был успешно привязан к вашей учётной записи!", color=int(f["preferredColor"]["primaryColor"], 16))
            embed.set_thumbnail(url=f["displayPicRaw"])
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"При добавлении возникла ошибка {e}.\nВозможно, вы неверно указали Gamertag.")
    
def setup(bot):
    bot.add_cog(Xbox(bot))