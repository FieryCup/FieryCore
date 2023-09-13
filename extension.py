import logging

import discord
from discord import app_commands
from discord.app_commands import Cooldown
from discord.app_commands.checks import _create_cooldown_decorator, cooldown
from discord.app_commands.commands import Check
from discord.ext import commands

from error_handler import error_handler
from libs.FieryCore import FieryBot


class Extension(commands.Cog):

    def __init__(self, child_object: object, file_name: str, bot: FieryBot):
        self.logger = logging.getLogger(f"bot.ext.{file_name.split('.')[-1]}")
        self.logger.debug(f'Initializing {child_object.__cog_name__} ...')
        self.bot = bot
        self.config = self.bot.config
        self.localizer = self.bot.localizer
        # self.database = self.bot.database

    # async def on_error(self, interaction: discord.Interaction,
    #                    error: app_commands.AppCommandError):
    async def on_error(self, *args):
        # await interaction.response.send_message(error, ephemeral=True)
        if len(args) == 3:
            await error_handler(self.bot, extension=args[0], interaction=args[1], error=args[2])
        else:
            await error_handler(self.bot, extension=None, interaction=args[0], error=args[1])

    @commands.Cog.listener()
    async def on_ready(self):
        def setup_command(path: str, command):
            if isinstance(command, app_commands.commands.Group):
                for command in command.commands:
                    setup_command(f"{path}.{command.name}", command)
                return

            cooldown = self.config[f'{path}.cooldown']
            key_func = lambda interaction: interaction.__getattribute__(cooldown["type"]).id

            command.checks = []
            app_commands.checks.cooldown(rate=cooldown["rate"], per=cooldown["per"], key=key_func)(command)

            command.on_error = self.on_error

        for command in self.__cog_app_commands__:
            setup_command(f"extensions.{self.__cog_name__.lower()}.commands.{command.name}", command)
            # if isinstance(command, app_commands.commands.Group):
            #     for command in command.commands:
            #         cooldown = self.config[f'extensions.{self.__cog_name__.lower()}.commands.{command.name}.cooldown']
            #         key_func = lambda interaction: interaction.__getattribute__(cooldown["type"]).id
            #
            #         command.checks = []
            #         app_commands.checks.cooldown(rate=cooldown["rate"], per=cooldown["per"], key=key_func)(command)
            #
            #         command.on_error = self.on_error
