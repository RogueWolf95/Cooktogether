from nextcord.ext import commands
import nextcord
import datetime
from src.discord.cogs.core.components.sqlite import DBManager
from src.discord.bot import DiscordBot


class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.db_manager = DBManager('src/discord/cogs/core/components/sql/core.db')
        self.name = "Admin Commands"
        print("CoreCog connected")


    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="kill", description="Kill the bot")
    async def bot_shutdown(self, interaction: nextcord.Interaction) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.bot_shutdown at {datetime.datetime.now()}")
        """Kill the bot, requiring a manual reboot."""
        await interaction.send(f"Shutdown command sent from {interaction.user}")
        await self.bot.close()
        
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="test", description="Kill the bot")
    async def test(self, interaction: nextcord.Interaction,user_input:str) -> None:
        print("WARNING", f"{interaction.user.name} used AdminCog.bot_shutdown at {datetime.datetime.now()}")
        """Kill the bot, requiring a manual reboot."""
        await interaction.send(user_input)



def setup(bot: commands.Bot):
    bot.add_cog(CoreCog(bot))