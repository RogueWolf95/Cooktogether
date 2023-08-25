from nextcord.ext import commands
import nextcord
import datetime
import re
from src.discord.bot import DiscordBot
from src.discord.cogs.core.components.modals import register
from src.discord.helpers import json_manager

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

    # =================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="kill", description="Kill the bot")
    async def bot_shutdown(self, interaction: nextcord.Interaction) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.bot_shutdown at {datetime.datetime.now()}")
        """Kill the bot"""
        await interaction.send(f"Shutdown command sent from {interaction.user}")
        await self.bot.close()

    # =================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="test", description="Test command")
    async def test(self, interaction: nextcord.Interaction,user_input:str) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.test at {datetime.datetime.now()}")
        """Test command"""
        await interaction.send(user_input)

    # =================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="valhalla", description="Valhalla test command")
    async def valhalla(self, interaction: nextcord.Interaction,user_input:str) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.valhalla test at {datetime.datetime.now()}")
        """Test command"""
        await interaction.send(user_input)

    # =================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="rate_recipe", description="Rate a recipe")
    async def rate(self, interaction: nextcord.Interaction, recipe_name:str, rating: int) -> None:
        print("WARNING", f"{interaction.user.name} used CoreCog.rate_recipe at {datetime.datetime.now()}")

        if rating < 1 or rating > 5:
            await interaction.send(" Invalid rating. Please provide a rating between 1 and 5.")
            return

        try:
            recipe_dict = json_manager.open_json(f"src/recipes/{recipe_name}.json")
        except FileNotFoundError:
            await interaction.send(f"Recipe not found check name\n{recipe_name}")
            return -1

        if "ratings" not in recipe_dict.keys():
            recipe_dict["ratings"] = {
                interaction.user.id: rating
            }
        else:
            recipe_dict["ratings"][str(interaction.user.id)] = rating
        
        json_manager.save_json(f"src/recipes/{recipe_name}.json", recipe_dict)
        await interaction.send(f" Thank you for submitting '{recipe_name}' with {rating} stars!")
    
    # =================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="convert", description="Convert a value from one unit to another")
    async def convert(self, interaction: nextcord.Interaction, value: float, from_unit: str, to_unit: str) -> None:
        print("WARNING", f"{interaction.user.name} used CoreCog.convert at {datetime.datetime.now()}")

        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        conversion_key = f"{from_unit}_to_{to_unit}"

        if conversion_key in self.conversion_rates:
            converted_value = value * self.conversion_rates[conversion_key]
            embed = nextcord.Embed(title="Conversion Result", description=f"{value} {from_unit} is {converted_value} {to_unit}", color=nextcord.Color.blurple())
            await interaction.send(embed=embed)
        else:
            await interaction.send(f"Sorry, I can't convert from {from_unit} to {to_unit}.")

    def convert_measurements_in_recipe(self, recipe, to_unit):
        conversions = [
            ("grams", "ounces", 0.035274),
            ("ounces", "grams", 28.3495),
            ("teaspoons", "tablespoons", 0.333333),
            ("tablespoons", "teaspoons", 3),
            ("cups", to_unit, 16),  # Convert "cups" to the provided to_unit
        ]

        for from_unit, dest_unit, conversion_rate in conversions:
            pattern = f"([0-9.]+) {from_unit}"
            replacement = lambda match: f"{float(match.group(1)) * conversion_rate} {dest_unit}"
            recipe = re.sub(pattern, replacement, recipe)

        return recipe

    @nextcord.slash_command(dm_permission=False, name="convert_recipe", description="Convert all measurements in a recipe")
    async def convert_recipe(self, interaction: nextcord.Interaction, *, recipe_and_unit: str) -> None:
        print("WARNING", f"{interaction.user.name} used CoreCog.convert_recipe at {datetime.datetime.now()}")

        recipe, to_unit = map(str.strip, recipe_and_unit.split(":"))

        converted_recipe = self.convert_measurements_in_recipe(recipe, to_unit)

        embed = nextcord.Embed(title="Converted Recipe", description=converted_recipe, color=nextcord.Color.blurple())
        await interaction.send(embed=embed)

  # =================================================================================================
    @nextcord.slash_command(dm_permission=False, name="register", description="Register to the bot for our newsletter")
    async def register(self, interaction: nextcord.Interaction) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.register at {datetime.datetime.now()}")
        """Register to the bot for our newsletter"""
        await interaction.response.send_modal(modal=RegisterModal())

# =====================================================================================================
def setup(bot: commands.Bot):
    bot.add_cog(CoreCog(bot))
