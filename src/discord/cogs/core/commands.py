from nextcord.ext import commands
import nextcord
import datetime
from src.discord.bot import DiscordBot


# =====================================================================================================
class RegisterModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="Register Newsletter")

    @nextcord.ui.button(label='Register', style=nextcord.ButtonStyle.primary)
    async def register_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("You are now registered!")

# =====================================================================================================
class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Admin Commands"
        print("CoreCog connected")
        
 
        self.conversion_rates = {
            "grams_to_ounces": 0.035274,
            "ounces_to_grams": 28.3495,
            "teaspoons_to_tablespoons": 0.333333,
            "tablespoons_to_teaspoons": 3,
            "cups_to_teaspoons": 48,
            "teaspoons_to_cups": 0.0208333,
            "cups_to_tablespoons": 16,
            "tablespoons_to_cups": 0.0625,

        }

# =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="kill", description="Kill the bot")
    async def bot_shutdown(self, interaction: nextcord.Interaction) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.bot_shutdown at {datetime.datetime.now()}")
        await interaction.send(f"Shutdown command sent from {interaction.user}")
        await self.bot.close()

# =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="test", description="Test command")
    async def test(self, interaction: nextcord.Interaction,user_input:str) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.test at {datetime.datetime.now()}")
        await interaction.send(user_input)

# =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="valhalla", description="Valhalla test command")
    async def valhalla(self, interaction: nextcord.Interaction,user_input:str) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.valhalla test at {datetime.datetime.now()}")
        await interaction.send(user_input)

# =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="rate", description="Rate a recipe")
    async def rate(self, interaction: nextcord.Interaction, user_input: str) -> None:
        print("WARNING", f"{interaction.user.name} usedAdminCog.rated at {datetime.datetime.now()}")
        await interaction.send(user_input)

# =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="favorites", description="Favorite Recipes")
    async def favorite(self, interaction: nextcord.Interaction, user_input: str) -> None:
        print("WARNING", f"{interaction.user.name} usedAdminCog.Favorite Recipes at {datetime.datetime.now()}")
        await interaction.send(user_input)

# =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="convert", description="Convert a value from one unit to another")
    async def convert(self, interaction: nextcord.Interaction, value: float, from_unit: str, to_unit: str) -> None:
        print("WARNING", f"{interaction.user.name} used CoreCog.convert at {datetime.datetime.now()}")
        
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        conversion_key = f"{from_unit}_to_{to_unit}"

        if conversion_key in self.conversion_rates:
            converted_value = value * self.conversion_rates[conversion_key]
            await interaction.send(f"{value} {from_unit} is {converted_value} {to_unit}")
        else:
            await interaction.send(f"Sorry, I can't convert from {from_unit} to {to_unit}.")

# =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="register", description="Register to the bot for our newsletter")
    async def register(self, interaction: nextcord.Interaction) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.register at {datetime.datetime.now()}")
        await interaction.response.send_modal(modal=RegisterModal())

# =====================================================================================================


def setup(bot: commands.Bot):
    bot.add_cog(CoreCog(bot))

