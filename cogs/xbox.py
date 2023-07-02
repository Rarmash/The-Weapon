import requests
import discord
import json
from discord.ext import commands
from discord.commands import SlashCommandGroup
from options import xboxapi

def get_user_info(gamertag):
    response = requests.get(f'https://xbl.io/api/v2/search/{gamertag}', headers={'x-authorization': xboxapi})
    response = response.json()[u"people"][0]
    return response

class Xbox(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    xbox = SlashCommandGroup("xbox", "Команды Xbox")

    @xbox.command(description='Посмотреть статистику по пользователю')
    async def stats(self, ctx: discord.ApplicationContext, gamertag):
        try:
            f = get_user_info(gamertag)
            embed = discord.Embed(title=f'Статистика игрока {f["gamertag"]}', color=int(f["preferredColor"]["primaryColor"], 16))
            embed.add_field(name="Gamerscore", value=f'{f["gamerScore"]}')
            embed.add_field(name="Репутация Xbox One", value=f'{f["xboxOneRep"]}')
            embed.add_field(name="Статус", value=f'{f["detail"]["accountTier"]}')
            embed.add_field(name="Фолловеров", value=f'{f["detail"]["followerCount"]}')
            embed.add_field(name="Друзей", value=f'{f["detail"]["followingCount"]}')
            embed.set_thumbnail(url=f["displayPicRaw"])
            await ctx.respond(embed = embed)
        except KeyError as e:
            await ctx.respond(f"❓ Возникла ошибка {e}...", ephemeral=True)
    
def setup(bot):
    bot.add_cog(Xbox(bot))