import discord
from discord.ext import commands
from options import accent_color
from datetime import date, datetime
from serverEvents import *

class Special(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot
    
    @commands.slash_command(description='Текущий эвент на сервере')
    async def event(self, ctx: discord.ApplicationContext):
        now = datetime.now()
        if datetime.strptime(serverEventsDates[0], '%d.%m.%Y %H:%M') < now < datetime.strptime(serverEventsDates[1], '%d.%m.%Y %H:%M'):
            eventEmbed = discord.Embed(
                title="Текущее событие: конкурс на новогоднюю аватарку для бота Оружие",
                description=f"Правила конкурса:\n— Работа должна быть авторской (не допускается работа, скопированная из интернета)\n— Одна работа на одного человека. Если два человека отправят одну и ту же работу, учитываться она будет у первого. Но: работа может создаваться совместно (в таком случае, указывайте не один тег в заявке, а два и более, каждый в отдельном поле)\n— Работа может быть как полностью создана с нуля, так и посредством программ по редактированию фотографий, к примеру, Photoshop.\n— Наполнение работы может быть любое, но тематика должна сохраняться, а именно Оружие и новогоднее оформление.\n— Работа не должна содержать контент 18+.\n— Прием работ осуществляется до <t:{str(datetime.strptime(serverEventsDates[1], '%d.%m.%Y %H:%M').timestamp())[:-2]}:f>.\n\nТе работы, что не удовлетворяют условиям, будут игнорироваться.\n\nВсем удачи в конкурсе!",
                color = accent_color
            )
            eventEmbed.set_thumbnail(url="https://avatars.mds.yandex.net/get-forms/6197807/55829197f633f8cf6b1202869b68f0d7/720x")
            eventEmbed.add_field(name="Ссылка на форму", value="[Тык](https://forms.yandex.ru/u/637b6098c769f1ad740ad57a/)")
            eventEmbed.add_field(name="Событие закончится", value=f"<t:{str(datetime.strptime(serverEventsDates[1], '%d.%m.%Y %H:%M').timestamp())[:-2]}:R>")
        else:
            eventEmbed = discord.Embed(
                description="Сейчас на сервере не проходит никакое событие!",
                color = accent_color
            )
        await ctx.respond(embed = eventEmbed)
        
    
def setup(bot):
    bot.add_cog(Special(bot))