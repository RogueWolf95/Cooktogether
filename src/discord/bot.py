import os

from nextcord import Intents
from nextcord.ext import commands

class DiscordBot(commands.Bot):
    intents = Intents.default()
    intents.message_content = True
    intents.members = True
    prefix = commands.when_mentioned

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=DiscordBot.prefix, intents=DiscordBot.intents, *args, **kwargs)
        # setup intents for bot permissions
        self.name = os.getenv("APP_NAME")
        self.version = os.getenv("APP_VERSION")
        self.app_title = f"{self.name} Discord Bot v.{self.version}"
        self.width = len(self.app_title) + 8
        self.primary_symbol = "="
        self.secondary_symbol = "-"
        self.settings = None

        self.IDX_REACTIONS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
        self.OPTIONS_REACTIONS = ["💾", "⭐", "♥️"]
        self.LOGO_PATH = "src/images/Logo1_printer.png"

        print("bot running")
        self.load_cogs()


    def load_cogs(self):
        all_extension_folders = [i for i in os.listdir("src/discord/cogs")]

        for folder in all_extension_folders:
            cogs = [i.removesuffix(".py") for i in os.listdir(f"src/discord/cogs/{folder}") if i.endswith(".py")]
            for extension in cogs:
                self.load_extension(f"src.discord.cogs.{folder}.{extension}")
