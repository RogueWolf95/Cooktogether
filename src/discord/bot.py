import json
import os
from typing import Dict

from nextcord import Intents, Member, Message
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

        print("bot running")
        self.load_cogs()


    def load_cogs(self):
        all_extensions = [i.removesuffix(".py") for i in os.listdir("src/discord/cogs") if i.endswith(".py")]
        for extension in all_extensions:
            self.load_extension(f"src.discord.cogs.{extension}")
