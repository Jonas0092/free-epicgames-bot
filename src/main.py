import asyncio
from asyncio import AbstractEventLoop
from threading import Thread

from dotenv import load_dotenv
import os

import epicgames
from fluxer_bot import FluxerBot


async def hello(ctx) -> None:
    await ctx.channel.send(f"Hello {ctx.author}!")


def main() -> None:
    load_dotenv()

    bot = FluxerBot()
    bot.add_command("hello", hello)

    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    check_interval = int(os.getenv("FREE_GAMES_CHECK_INTERVAL"))
    if not check_interval or check_interval <= 0:
        check_interval = 3600

    Thread(target=check_free_games_loop, args=(bot, check_interval, event_loop)).start()

    token: str = os.getenv("BOT_TOKEN")

    bot.start(token, event_loop)


async def check_free_games_loop_async(bot: FluxerBot, check_interval: int) -> None:
    channel_id = int(os.getenv("CHANNEL_ID"))

    while True:
        new_free_games: list[dict] = epicgames.get_new_free_games()
        if len(new_free_games) > 0:
            message: str = build_free_games_message(new_free_games)
            await bot.send_message(channel_id, message)

        await asyncio.sleep(check_interval)


def check_free_games_loop(bot: FluxerBot, check_interval: int, event_loop: AbstractEventLoop) -> None:
    asyncio.run_coroutine_threadsafe(check_free_games_loop_async(bot, check_interval), event_loop)


def build_free_games_message(games: list[dict]) -> str:
    message = "### Free Games:\n"
    for game in games:
        message += f"**{game['title']}**\n{game['description']}\n\n"
    return message.strip()


if __name__ == "__main__":
    main()
