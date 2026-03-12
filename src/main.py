import asyncio

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

    token: str = os.getenv("BOT_TOKEN")

    bot.start(token, event_loop)


if __name__ == "__main__":
    main()
