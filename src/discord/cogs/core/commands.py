from nextcord.ext import commands
import nextcord
import datetime
import inspect
from typing import Optional
from src.discord.bot import DiscordBot
from src.discord.cogs.core.components.modals import register


class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Admin Commands"
        print("CoreCog connected")

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="register", description="Register to the bot for our newsletter")
    async def register(self, interaction: nextcord.Interaction) -> None:
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """Register to the bot for our newsletter"""
        await interaction.response.send_modal(modal=register.RegisterModal())
        
    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="kill", description="Kill the bot")
    async def bot_shutdown(self, interaction: nextcord.Interaction) -> None:
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """Kill the bot, requiring a manual reboot."""
        await interaction.send(f"Shutdown command sent from {interaction.user}")
        await self.bot.close()
    
    # =====================================================================================================    
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="test", description="Test command")
    async def test(self, interaction: nextcord.Interaction,user_input:str) -> None:
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """Test command."""
        await interaction.send(user_input)

    # =====================================================================================================    
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="valhalla", description="Valhalla test command")
    async def valhalla(self, interaction: nextcord.Interaction,user_input:str) -> None:
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """Valhalla test command."""
        await interaction.send(user_input)
        
    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="rate", description="Rate a recipe")
    async def rate(self, interaction: nextcord.Interaction, user_input: str) -> None:
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """Kill the bot, requiring a manual reboot."""
        await interaction.send(user_input)
        
    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="Favorites", description="Favorite Recipes")
    async def favorite(self, interaction: nextcord.Interaction, user_input: str) -> None:
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """Kill the bot, requiring a manual reboot."""
        await interaction.send(user_input)
        
    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False,name="convert",description="Convert measurements between units")
    async def convert(self, interaction: nextcord.Interaction, amount: float, from_unit: str, to_unit: str) -> None:
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """Convert measurements between units."""
        converted_amount = self.perform_unit_conversion(amount, from_unit, to_unit)
        if converted_amount is not None:
            response = f"{amount} {from_unit} is equal to {converted_amount:.2f} {to_unit}"
        else:
            response = "Unsupported units or conversion error."
        await interaction.send(response)

    def perform_unit_conversion(self, amount: float, from_unit: str, to_unit: str) -> Optional[float]:
        conversions = {
            ("grams", "ounces"): lambda x: x * 0.03527396,
            ("ounces", "grams"): lambda x: x / 0.03527396,
            ("cups", "milliliters"): lambda x: x * 236.588,
            ("milliliters", "cups"): lambda x: x / 236.588,
            ("teaspoons", "tablespoons"): lambda x: x / 3,
            ("tablespoons", "teaspoons"): lambda x: x * 3,
        }

        conversion_func = conversions.get((from_unit, to_unit))
        if conversion_func:
            converted_amount = conversion_func(amount)
            return converted_amount
        else:
            raise ValueError("Conversion error.")

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="register", description="Register to the bot for our newsletter")
    async def register(self, interaction: nextcord.Interaction) -> None:
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """Register to the bot for our newsletter"""
        await interaction.response.send_modal(modal=register.RegisterModal())



def setup(bot: commands.Bot):
    bot.add_cog(CoreCog(bot))
