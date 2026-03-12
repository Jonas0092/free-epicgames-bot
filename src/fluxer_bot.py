from asyncio import AbstractEventLoop
from typing import Callable

import fluxer


class FluxerBot:
    """
    Wrapper class for Fluxer bots
    """

    def __init__(self, command_prefix: str = "!"):
        """
        Create a new FluxerBot
        :param command_prefix: Symbol to use as command prefix, default is '!'
        """
        self.__bot: fluxer.Bot = fluxer.Bot(command_prefix=command_prefix, intents=fluxer.Intents.default())

        @self.__bot.event
        async def on_ready():
            print(f"Logged in as {self.__bot.user.username}")

    def start(self, token: str, event_loop: AbstractEventLoop) -> None:
        """
        Start the bot
        :param token: Token of the Fluxer application to connect his bot to
        :param event_loop: The event loop to use
        """
        async def runner():
            try:
                await self.__bot.start(token)
            except KeyboardInterrupt:
                pass
            finally:
                await self.__bot.close()

        event_loop.run_until_complete(runner())

    def add_command(self, name: str, function: Callable) -> None:
        """
        Add a command for the bot.
        The command can be used by sending {command_prefix}{name} to a Fluxer channel which the bot can see.
        :param name: The name of the command
        :param function: The function to execute when the command is used; has to be asynchronous
        """
        @self.__bot.command(name=name)
        async def command(ctx) -> None:
            await function(ctx)
