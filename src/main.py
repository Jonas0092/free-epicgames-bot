import asyncio
from asyncio import AbstractEventLoop
from dotenv import load_dotenv
import os
from threading import Thread

import epicgames
from fluxer_bot import FluxerBot


# Default interval between checks for new free games (in seconds)
DEFAULT_CHECK_INTERVAL: int = 3600


def main() -> None:
    # Load environment variables from .env file
    load_dotenv()

    bot: FluxerBot = FluxerBot()

    # Create event loop
    event_loop: AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    # Get interval between free game checks
    check_interval: int = get_check_interval()

    # Start free game check loop
    check_loop_thread: Thread = Thread(target=check_free_games_loop, args=(bot, check_interval, event_loop))
    check_loop_thread.start()

    # Start bot
    token: str = os.getenv("BOT_TOKEN")
    bot.start(token, event_loop)


def get_check_interval() -> int:
    check_interval_var: str | None = os.getenv("FREE_GAMES_CHECK_INTERVAL")
    if not check_interval_var:
        return DEFAULT_CHECK_INTERVAL

    check_interval: int = int(check_interval_var)
    if check_interval <= 0:
        return DEFAULT_CHECK_INTERVAL

    return check_interval


async def check_free_games_loop_async(bot: FluxerBot, check_interval: int) -> None:
    channel_id: int = int(os.getenv("CHANNEL_ID"))

    while True:
        # Retrieve new free games
        new_free_games: list[dict] = epicgames.get_new_free_games()

        if len(new_free_games) > 0:
            # Send message
            message: str = build_free_games_message(new_free_games)
            await bot.send_message(channel_id, message)

        await asyncio.sleep(check_interval)


def check_free_games_loop(bot: FluxerBot, check_interval: int, event_loop: AbstractEventLoop) -> None:
    asyncio.run_coroutine_threadsafe(check_free_games_loop_async(bot, check_interval), event_loop)


def build_free_games_message(games: list[dict]) -> str:
    message: str = "### Free Games:\n"
    for game in games:
        message += f"**{game['title']}**\n{game['description']}\n\n"
    return message.strip()


if __name__ == "__main__":
    main()
