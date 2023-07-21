from dotenv import load_dotenv
from os import getenv

from src.discord.bot import DiscordBot

def main():
    load_dotenv()
    bot = DiscordBot()
    bot.run(getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    main()