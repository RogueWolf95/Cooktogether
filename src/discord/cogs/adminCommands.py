from nextcord.ext import commands
import nextcord
import datetime
from src.discord.bot import DiscordBot


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot: DiscordBot = bot
        self.name = "Admin Commands"

    # =====================================================================================================
    @nextcord.slash_command(default_member_permissions=8, dm_permission=False, name="kill", description="Kill the bot")
    async def bot_shutdown(self, interaction: nextcord.Interaction) -> None:
        print("WARNING", f"{interaction.user.name} used CoreCog.kill at {datetime.datetime.now()}")
        """Kill the bot, requiring a manual reboot."""
        await interaction.send(f"Shutdown command sent from {interaction.user}")
        await self.bot.close()



def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))