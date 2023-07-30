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
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="bot_shutdown", description="shutdown the bot")   # this information is seen by discord
    async def bot_shutdown(self, interaction: nextcord.Interaction, user_input: str) -> None:                                                          # interaction is context sent from discord
        print("WARNING", f"{interaction.user.name} used AdminCog.bot_shutdown at {datetime.datetime.now()}")                          # this is a terminal output showing who used the command and when
        """Shutdown the bot, requiring a manual reboot."""
        await interaction.send(f"Shutdown command sent from {interaction.user}")                                                      # sends a message in discord with the user name who sent the command
        await self.bot.close()                                                                                                        # close the bot shutting it down



def setup(bot: commands.Bot):
    bot.add_cog(CoreCog(bot))