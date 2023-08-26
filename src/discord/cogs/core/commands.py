from nextcord.ext import commands
import nextcord
import datetime
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
class ConversionSelect(nextcord.ui.Select):
    def __init__(self, value, unit, conversion_table):
        self.value = value
        self.unit = unit
        self.conversion_table = conversion_table
        options = [
            nextcord.SelectOption(label=target_unit, description=f"Convert {value} {unit} to {target_unit}")
            for target_unit in conversion_table[unit]
        ]
        super().__init__(placeholder=f"Select a unit to convert {unit} to", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        target_unit = self.values[0]
        converted_value = self.value * self.conversion_table[self.unit][target_unit]
    
        formatted_conversion = f"{self.value:.1f} {self.unit} is {converted_value:.1f} {target_unit}"

        embed = nextcord.Embed(title="Measurement Conversion", color=nextcord.Color.blue())
        embed.add_field(name="Conversion Result", value=formatted_conversion, inline=True)

        await interaction.response.send_message(embed=embed)

class ConversionView(nextcord.ui.View):
    def __init__(self, value, unit, conversion_table, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(ConversionSelect(value, unit, conversion_table))

# =====================================================================================================
class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Admin Commands"
        print("CoreCog connected")
        
        self.ingredient_swaps = {
            "egg": {
                "quantity": "1 egg",
                "substitutes": [
                    "1/2 mashed banana (adds sweetness)",
                    "1/4 cup applesauce (for baking)",
                    "1 tablespoon ground flaxseed + 3 tablespoons water (let sit for 5 minutes before using)"
                ]
            },
            "butter": {
                "quantity": "1 cup",
                "substitutes": [
                    "1/2 cup mashed avocado",
                    "1 cup coconut oil",
                    "1 cup Greek yogurt (for baking)"
                ]
            },
            "milk": {
                "quantity": "1 cup",
                "substitutes": [
                    "1 cup almond milk",
                    "1 cup soy milk",
                    "1 cup coconut milk"
                ]
            },
            "sugar": {
                "quantity": "1 cup",
                "substitutes": [
                    "3/4 cup honey (reduce other liquid by 1/4 cup)",
                    "3/4 cup maple syrup (reduce other liquid by 3 tbsp)",
                    "1 cup coconut sugar"
                ]
            },
            "bread crumbs": {
                "quantity": "1 cup",
                "substitutes": [
                    "1 cup crushed crackers",
                    "1 cup oatmeal",
                    "1 cup quinoa flakes"
                ]
            },
            "flour": {
                "quantity": "1 cup (all-purpose flour)",
                "substitutes": [
                    "1 cup whole wheat flour",
                    "1/2 cup coconut flour + 1/4 cup more liquid",
                    "1 cup almond flour"
                ]
            },
            "chocolate": {
                "quantity": "1 ounce",
                "substitutes": [
                    "1 ounce unsweetened baking chocolate + 1 tbsp sugar",
                    "1 ounce semi-sweet chocolate chips",
                    "1 tbsp cocoa powder + 2 tsp sugar + 2 tsp unsalted butter"
                ]
            },
            "wine": {
                "quantity": "1 cup",
                "substitutes": [
                    "1 cup chicken or beef broth",
                    "1 cup fruit juice",
                    "1 cup water + 1 tbsp vinegar or lemon juice"
                ]
            }
        }

        self.conversion_table = {
            "cups": {"tablespoons": 16, "teaspoons": 48, "ounces": 8, "milliliters": 236.59, "liters": 0.23659},
            "tablespoons": {"teaspoons": 3, "ounces": 0.5, "milliliters": 14.79, "liters": 0.01479, "cups": 0.0625},
            "teaspoons": {"tablespoons": 0.3333, "ounces": 0.1667, "milliliters": 4.93, "liters": 0.00493, "cups": 0.02083},
            "ounces": {"tablespoons": 2, "teaspoons": 6, "cups": 0.125, "milliliters": 29.57, "liters": 0.02957, "grams": 28.35},
            "grams": {"milligrams": 1000, "ounces": 0.0353}
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
    @nextcord.slash_command(dm_permission=False, name="register", description="Register to the bot for our newsletter")
    async def register(self, interaction: nextcord.Interaction) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.register at {datetime.datetime.now()}")
        """Register to the bot for our newsletter"""
        await interaction.response.send_modal(modal=RegisterModal())

# =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="substitute", description="Get substitutions for ingredients")
    async def substitute(self, interaction: nextcord.Interaction, ingredient: str) -> None:
        ingredient = ingredient.lower()

        if ingredient in self.ingredient_swaps:
            substitutes_list = "\n".join(f"{idx+1}. {sub}" for idx, sub in enumerate(self.ingredient_swaps[ingredient]['substitutes']))

            embed = nextcord.Embed(
                title=f"Substitutes for {self.ingredient_swaps[ingredient]['quantity']}",
                description=substitutes_list,
                color=nextcord.Color.green()
            )
            await interaction.send(embed=embed)
        else:
            await interaction.send(f"I'm sorry, I don't have substitutes for {ingredient} right now.")

# =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="convert", description="Convert measurements")
    async def convert(self, interaction: nextcord.Interaction, amount: float, unit: str) -> None:
        unit = unit.lower()
        if unit in self.conversion_table:
            view = ConversionView(amount, unit, self.conversion_table)
            await interaction.send(f"Select the unit you want to convert {unit} to:", view=view)
        else:
            await interaction.send(f"I'm sorry, I don't have conversions for {unit} right now.")

   
# =====================================================================================================
def setup(bot: commands.Bot):
    bot.add_cog(CoreCog(bot))

