import asyncio
from asyncio import AbstractEventLoop
from threading import Thread

from dotenv import load_dotenv
import os

from fluxer_bot import FluxerBot


async def hello(ctx) -> None:
    await ctx.channel.send(f"Hello {ctx.author}!")


def main() -> None:
    load_dotenv()

    bot = FluxerBot()
    bot.add_command("hello", hello)

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    Thread(target=send_message, args=(bot, event_loop)).start()

    token: str = os.getenv("BOT_TOKEN")

    bot.start(token, event_loop)


def send_message(bot: FluxerBot, event_loop: AbstractEventLoop) -> None:
    channel_id = int(os.getenv("CHANNEL_ID"))
    asyncio.run_coroutine_threadsafe(bot.send_message(channel_id, "Hello World!"), event_loop)


if __name__ == "__main__":
    main()
