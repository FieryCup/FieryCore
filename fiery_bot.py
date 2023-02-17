import logging
from typing import Any

from discord.ext.commands import Bot, ExtensionFailed

__all__ = {"FieryBot"}

logger = logging.getLogger("bot.core")


class FieryBot(Bot):

    def __init__(self, extensions: list[str], command_prefix: str, extensions_path: str = "ext", **options: Any):
        """
        Custom bot for FieryCore

        :param extensions: List of extension names
        :param command_prefix: Command prefix
        :param extensions_path: The path to extensions through a point, for example: core.extensions
        :param options:
        """
        self.extensions_list = extensions
        self.extensions_path = extensions_path

        super().__init__(command_prefix, **options)

    async def setup_hook(self) -> None:
        # TODO: Refactor setup_hook()
        logger.info("Loading extensions ...")

        loaded_extensions = []
        not_loaded_extensions = []
        for extension in self.extensions_list:
            try:
                await self.load_extension(f"{self.extensions_path}.{extension}")
            except ExtensionFailed as err:
                logger.error(f"Extension {self.extensions_path}.{extension} caused an error",
                             exc_info=err)
                not_loaded_extensions.append(extension)
            else:
                loaded_extensions.append(extension)

        if loaded_extensions:
            logger.info(f"Loaded extensions: {', '.join(loaded_extensions)}")
        else:
            logger.info("No loaded extensions")

        if not_loaded_extensions:
            logger.warning(f"Error whilst loaded extensions: "
                           f"{', '.join(not_loaded_extensions)}")
        else:
            logger.info("No errored extensions")

        logger.info("Syncing commands...")
        await self.tree.sync()
        synced_commands = [command.qualified_name for command
                           in self.tree.get_commands()]
        logger.info(f"Synchronized commands: {', '.join(synced_commands)}")

    async def on_ready(self):
        logger.info(f"Logged into: {self.user} ({self.user.id})")

    async def close(self):
        logger.info("The end of logs")
        await super().close()
