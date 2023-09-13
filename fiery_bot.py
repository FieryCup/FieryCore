import logging
from typing import Any, Optional

import discord.app_commands
from discord import app_commands
from discord.ext.commands import ExtensionFailed, AutoShardedBot

__all__ = {"FieryBot"}

from libs.Config import Config
# from libs.DatabaseAPI import Database
from libs.Localizer import Localizer

logger = logging.getLogger("bot.core")


class FieryBot(AutoShardedBot):

    def __init__(self, extensions: list[str],
                 command_prefix: str,
                 extensions_path: str = "ext",
                 localizer_path: str = "lang",
                 config_path: str = "config.yaml",
                 reset_commands: bool = True,
                 **options: Any):
        """
        Custom bot for FieryCore

        :param extensions: List of extension names
        :param command_prefix: Command prefix
        :param extensions_path: The path to extensions through a point, for example: core.extensions
        :param localizer_path: The path to translations
        :param reset_commands: Reset commands
        :param translator: Translator
        :param options:
        """
        self.extensions_list = extensions
        self.extensions_path = extensions_path
        self.reset_commands = reset_commands

        self.config_path = config_path
        self.config = Config.load(self.config_path)

        self.localizer_path = localizer_path
        self.localizer = Localizer(self.localizer_path)

        database_config = self.config["database"]
        # self.database = Database(
        #     host=database_config["host"],
        #     user=database_config["user"],
        #     password=database_config["password"],
        # )

        self.loaded_extensions = []
        self.errored_extensions = []

        super().__init__(command_prefix, **options)

    async def load_ext(self, extension: str):
        try:
            await self.load_extension(f"{self.extensions_path}.{extension}")
        except ExtensionFailed as err:
            logger.error(f"Extension {self.extensions_path}.{extension} caused an error",
                         exc_info=err)
            self.errored_extensions.append(extension)
        else:
            self.loaded_extensions.append(extension)

    async def unload_ext(self, extension: str):
        try:
            await self.unload_extension(f"{self.extensions_path}.{extension}")
        except ExtensionFailed as err:
            logger.error(f"Extension {self.extensions_path}.{extension} caused an error",
                         exc_info=err)
        else:
            self.loaded_extensions.remove(extension)

    async def setup_hook(self) -> None:
        # TODO: Refactor setup_hook()

        # Reset commands
        if self.reset_commands:
            logger.info("Reset commands...")
            await self.tree.sync()

        await self.tree.set_translator(Localizer(self.localizer_path))

        # Loading extensions
        logger.info("Loading extensions ...")

        for extension in self.extensions_list:
            await self.load_ext(extension)

        if self.loaded_extensions:
            logger.info(f"Loaded extensions: {', '.join(self.loaded_extensions)}")
        else:
            logger.info("No loaded extensions")

        if self.errored_extensions:
            logger.warning(f"Error whilst loaded extensions: "
                           f"{', '.join(self.errored_extensions)}")
        else:
            logger.info("No errored extensions")

        # Syncing commands
        logger.info("Syncing commands...")

        await self.tree.sync()

        synced_commands = [command.qualified_name for command
                           in self.tree.get_commands()]

        if synced_commands:
            logger.info(f"Synchronized commands: {', '.join(synced_commands)}")
        else:
            logger.info("No synchronized commands")

    async def on_ready(self):
        logger.info(f"Logged into: {self.user} ({self.user.id})")

    async def close(self):
        logger.info("End of logs")
        await super().close()
