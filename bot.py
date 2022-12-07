import os
from glob import glob

from discord import Intents

from serpent import Serpent


intents = Intents.all()
bot = Serpent(
    command_prefix=["."],
    config_filename="config/config.toml",
    intents=intents
)
logger = bot.logger
extensions = [i.replace(os.sep, '.')[:-3] for i in glob("cogs/*/[!_]*.py")]


if __name__ == "__main__":
    """Starts the bot, loading all of the extensions"""

    logger.info(f"Loading {len(extensions)} extensions")
    print(f"Loading {len(extensions)} extensions")
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded {extension} sucessfully")
        except Exception as e:
            print(f"Failed to load {extension}")
            raise e
    bot.run()
