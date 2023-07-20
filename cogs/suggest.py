import discord
from discord.ext import commands
from options import suggestions_channel, accent_color, SuggestionsCollection


class SuggestButtons(discord.ui.View):
    def __init__(self, suggestion_message_id, data):
        super().__init__(timeout=None)
        self.suggestion_message_id = suggestion_message_id
        self.data = data

    def update_buttons(self):
        accept_button = [x for x in self.children if x.custom_id == "accept"][0]
        deny_button = [x for x in self.children if x.custom_id == "deny"][0]
        accept_button.label = f"За ({self.data['accept_count']})"
        deny_button.label = f"Против ({self.data['deny_count']})"

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Check if the user has already voted on this suggestion
        if interaction.user.id in self.data["voted_users"]:
            await interaction.response.send_message("Вы уже проголосовали.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="За (0)", style=discord.ButtonStyle.green, emoji="<:MinecraftAccept:936636758135828502>", custom_id='accept')
    async def accept_button_callback(self, button, interaction):
        self.data["accept_count"] += 1
        self.data["voted_users"].append(interaction.user.id)
        self.update_buttons()
        await interaction.response.edit_message(view=self)

        # Update MongoDB data
        SuggestionsCollection.update_one(
            {"_id": self.suggestion_message_id},
            {"$set": self.data},
        )

    @discord.ui.button(label="Против (0)", style=discord.ButtonStyle.red, emoji="<:MinecraftDeny:936636758127439883>", custom_id='deny')
    async def deny_button_callback(self, button, interaction):
        self.data["deny_count"] += 1
        self.data["voted_users"].append(interaction.user.id)
        self.update_buttons()
        await interaction.response.edit_message(view=self)

        # Update MongoDB data
        SuggestionsCollection.update_one(
            {"_id": self.suggestion_message_id},
            {"$set": self.data},
        )


class Suggest(commands.Cog):
    def __init__(self, bot):
        self.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Fetch existing suggestion data from the database and add views for each suggestion
        all_suggestions = SuggestionsCollection.find()
        for suggestion_data in all_suggestions:
            suggestion_message_id = suggestion_data["_id"]
            channel = self.Bot.get_channel(suggestions_channel)
            if channel:
                try:
                    suggestion_message = await channel.fetch_message(suggestion_message_id)
                    suggest_buttons = SuggestButtons(suggestion_message_id, suggestion_data)
                    await suggestion_message.edit(view=suggest_buttons)
                except discord.NotFound:
                    print(f"Suggestion message with ID {suggestion_message_id} not found.")
            else:
                print(f"Suggestions channel with ID {suggestions_channel} not found.")

    @commands.slash_command(description='Предложить идею')
    async def suggest(self, ctx: discord.ApplicationContext, *, question):
        suggestEmbed = discord.Embed(title="Новое предложение", description=f"{question}", color=accent_color)
        suggestEmbed.add_field(
            name='Автор',
            value=f'<@{ctx.author.id}>'
        )
        suggestions_msg = await ctx.respond(embed=suggestEmbed)
        suggestions_message = await suggestions_msg.original_response()
        suggestion_data = {
            "_id": suggestions_message.id,
            "accept_count": 0,
            "deny_count": 0,
            "voted_users": []
        }
        SuggestionsCollection.insert_one(suggestion_data)
        suggest_buttons = SuggestButtons(suggestions_message.id, suggestion_data)
        await suggestions_message.edit(view=suggest_buttons)
        suggest_buttons.update_buttons()


def setup(bot):
    bot.add_cog(Suggest(bot))
