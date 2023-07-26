import discord
from discord.ext import commands
from options import servers_data
from time import sleep
import os

class TicketButtons(discord.ui.View):
    def __init__(self, bot, servers_data):
        super().__init__(timeout=None)
        self.Bot = bot
        self.servers_data = servers_data

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        server_data = self.servers_data.get(str(interaction.guild.id))
        if not server_data:
            return
        if not(discord.utils.get(interaction.guild.roles, id=server_data.get("elder_mod_role_id")) in interaction.user.roles or discord.utils.get(interaction.guild.roles, id=server_data.get("admin_role_id")) in interaction.user.roles):
            await interaction.response.send_message("У вас нет прав для выполнения данной команды.", ephemeral=True)
            return False
        return True

    @discord.ui.select(placeholder="Добавить пользователя", min_values=1, max_values=1, select_type=discord.ComponentType.user_select, custom_id="adduser")
    async def add_user_select_callback(self, select, interaction):
        await interaction.channel.set_permissions(select.values[0],speak=True,send_messages=True,read_message_history=True,read_messages=True)
        await interaction.response.send_message(f'<@{select.values[0].id}>, вас добавили в чат Тикета для решения вопроса.')

    @discord.ui.button(label="Закрыть тикет", style=discord.ButtonStyle.red, emoji="🔐", custom_id='closeticket')
    async def сlose_button_callback(self, button, interaction):
        server_data = self.servers_data.get(str(interaction.guild.id))
        if not server_data:
            return
        self.disable_all_items()
        await interaction.response.edit_message(view=self)
        embed = discord.Embed(description='Удаление Тикета через 10 секунд.', color=int(server_data.get("accent_color"), 16))
        await interaction.followup.send(embed=embed)
        sleep(10)
        filename=f'{interaction.channel.name}.txt'
        with open(filename, "w") as file:
            async for msg in interaction.channel.history(limit=None, oldest_first=True):
                msg_time = str(msg.created_at)[:-13]
                file.write(f"{msg_time} - {msg.author.display_name}: {msg.content}\n")
        channel = self.Bot.get_channel(server_data.get("admin_channel"))
        await channel.send(f'{interaction.channel.name} закрыт.', file=discord.File(filename))
        os.remove(filename)
        await interaction.channel.delete()

class Support(commands.Cog):
    def __init__(self, bot, servers_data):
        self.Bot = bot
        self.servers_data = servers_data
    
    @commands.slash_command(description='Отправить Тикет')
    async def ticket(self, ctx, text):
        server_data = self.servers_data.get(str(ctx.guild.id))
        if not server_data:
            return
        embed = discord.Embed(
            description=f'**<@{ctx.author.id}> открывает Тикет**\n**Причина:** {text}\n**В канале:** <#{ctx.channel.id}>',
            color=int(server_data.get("accent_color"), 16)
        )
        tcategory = discord.utils.get(ctx.guild.categories, id=server_data.get("ticket_category"))
        channel = await ctx.guild.create_text_channel(f'Ticket-<@{ctx.author.name}>', topic=text, category=tcategory)
        await channel.set_permissions(ctx.author,speak=True,send_messages=True,read_message_history=True,read_messages=True)
        await channel.send(f'<@&{server_data.get("elder_mod_role_id")}>ы, надо обкашлять пару вопросиков.', embed=embed, view=TicketButtons(self.Bot, servers_data))
        await channel.send(f'<@{ctx.author.id}>, вам слово.')
        embed = discord.Embed(description='Ваш Тикет был успешно отправлен!', color = int(server_data.get("accent_color"), 16))        
        await ctx.respond(embed = embed, ephemeral=True)
        
def setup(bot):
    bot.add_cog(Support(bot, servers_data))