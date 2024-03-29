import datetime
import logging
import os
import sys

import discord

from libs.FieryCore import FieryBot
from logger import Logger

__all__ = {"FieryCore"}

logging_dict = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'FATAL': logging.FATAL,
}

logger = logging.getLogger("bot.core")


class FieryCore:

    def __init__(
            self,
            application_id: int,
            extensions: list[str],
            extensions_path: str = "ext",
            localizer_path: str = "lang",
            config_path: str = "config.yaml",
            bot_log_path: str = "logs/bot.log",
            bot_log_level: logging = logging.INFO,
            discord_log_path: str = "logs/discord.log",
            discord_log_level: logging = logging.INFO,
            command_prefix: str = "fc.",
            activity: discord.Activity = discord.Activity(),
            status: discord.Status = discord.Status.online,
            intents: discord.Intents = discord.Intents().all(),
            reset_commands: bool = True,
            translator: discord.app_commands.Translator = None,
    ):
        """
        The core for the Discord bot

        :param application_id: Application ID
        :param extensions: List of bot extensions
        :param extensions_path: The path to extensions through a point, for example: core.extensions
        :param localizer_path: The path to translations
        :param config_path: The path to config
        :param bot_log_path: Path to the bot logs file
        :param bot_log_level: Bot logging level
        :param discord_log_path: The path to the Discord logs file
        :param discord_log_level: Discord logging level
        :param command_prefix: Command prefix
        :param activity: Bot activity
        :param status: Bot status
        :param intents: Bot intents
        :param reset_commands: Reset commands
        """
        self.application_id = application_id
        self.extensions = extensions
        self.extensions_path = extensions_path
        self.localizer_path = localizer_path
        self.config_path = config_path
        self.bot_log_path = bot_log_path
        self.bot_log_level = bot_log_level
        self.discord_log_path = discord_log_path
        self.discord_log_level = discord_log_level
        self.command_prefix = command_prefix
        self.activity = activity
        self.status = status
        self.intents = intents
        self.reset_commands = reset_commands

    def run(self, token: str) -> None:
        """
        Launches the Discord bot.

        :param token: The authentication token
        :return:
        """

        # Brief information about the Python and Discord versions
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Discord module version: {discord.__version__}")

        # Creating non-existent files
        if not os.path.exists(self.discord_log_path):
            with open(self.discord_log_path, "w"):
                pass
        if not os.path.exists(self.bot_log_path):
            with open(self.bot_log_path, "w"):
                pass

        # Creating loggers
        Logger(self.discord_log_level).set_logging(
            "discord", self.discord_log_path, True)
        Logger(self.bot_log_level).set_logging(
            "bot", self.bot_log_path, True)

        # Creating a bot
        bot = FieryBot(
            command_prefix=self.command_prefix,
            intents=self.intents,
            activity=self.activity,
            status=self.status,
            application_id=self.application_id,
            extensions=self.extensions,
            extensions_path=self.extensions_path,
            reset_commands=self.reset_commands,
            config_path=self.config_path,
            localizer_path=self.localizer_path,
        )

        # Launching the bot
        bot.run(token, log_handler=None)
