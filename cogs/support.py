import discord
from discord.ext import commands
from options import accent_color, mod_role_id, admin_channel, ticket_category
from time import sleep
import os

class TicketButtons(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.Bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if discord.utils.get(interaction.guild.roles, id=mod_role_id) not in interaction.user.roles:
            await interaction.response.send_message("У вас нет прав для выполнения данной команды.", ephemeral=True)
            return False
        return True

    @discord.ui.select(placeholder="Добавить пользователя", min_values=1, max_values=1, select_type=discord.ComponentType.user_select, custom_id="adduser")
    async def add_user_select_callback(self, select, interaction):
        await interaction.channel.set_permissions(select.values[0],speak=True,send_messages=True,read_message_history=True,read_messages=True)
        await interaction.response.send_message(f'<@{select.values[0].id}>, вас добавили в чат Тикета для решения вопроса.')

    @discord.ui.button(label="Закрыть тикет", style=discord.ButtonStyle.red, emoji="🔐", custom_id='closeticket')
    async def сlose_button_callback(self, button, interaction):
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        embed = discord.Embed(description='Удаление Тикета через 10 секунд.', color=accent_color)
        await interaction.followup.send(embed=embed)
        sleep(10)
        filename=f'{interaction.channel.name}.txt'
        with open(filename, "w") as file:
            async for msg in interaction.channel.history(limit=None, oldest_first=True):
                msg_time = str(msg.created_at)[:-13]
                file.write(f"{msg_time} - {msg.author.display_name}: {msg.content}\n")
        channel = self.Bot.get_channel(admin_channel)
        await channel.send(f'{interaction.channel.name} закрыт.', file=discord.File(filename))
        os.remove(filename)
        await interaction.channel.delete()

class Support(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot
    
    @commands.slash_command(description='Отправить Тикет')
    async def ticket(self, ctx, text):
        embed = discord.Embed(
            description=f'**<@{ctx.author.id}> открывает Тикет**\n**Причина:** {text}\n**В канале:** <#{ctx.channel.id}>',
            color=accent_color
        )
        tcategory = discord.utils.get(ctx.guild.categories, id=ticket_category)
        channel = await ctx.guild.create_text_channel(f'Ticket-<@{ctx.author.name}>', topic=text, category=tcategory)
        await channel.set_permissions(ctx.author,speak=True,send_messages=True,read_message_history=True,read_messages=True)
        await channel.send(f'<@&{mod_role_id}>ы, надо обкашлять пару вопросиков.', embed=embed, view=TicketButtons(self.Bot))
        await channel.send(f'<@{ctx.author.id}>, вам слово.')
        embed = discord.Embed(description='Ваш Тикет был успешно отправлен!', color = accent_color)        
        await ctx.respond(embed = embed, ephemeral=True)
        
def setup(bot):
    bot.add_cog(Support(bot))