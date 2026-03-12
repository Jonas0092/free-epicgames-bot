# Free Epic Games Bot
This is a simple [Fluxer](https://fluxer.app) bot that can notify you about free games on Epic Games.
It regularly retrieves the current free games and sends a message to a specified channel once there are new ones.

## Prerequisites
To run this bot, you first need to have a Fluxer account.
Then you have to create an application in Fluxer.
For details on how to do that, see steps 1-7 of this official guide:
[Fluxer Dev Quickstart Guide](https://docs.fluxer.app/quickstart). \
Tested with Python 3.13.5.

## Setup
- Install the dependencies listed in `requirements.txt`
- Create a `.env` file in the `src` directory with the following variables (or set them as environment variables):
  - `BOT_TOKEN=<your-bots-token>` \
  You get this when creating the application in Fluxer
  - `CHANNEL_ID=<channel-id>` \
  Use the ID of the channel you want the bot to send the notifications to
  - Optional: `FREE_GAMES_CHECK_INTERVAL=<interval-in-seconds>` \
  How often the bot should check for new games, defaults to 3600 (= 1 hour) if not set

## Running the bot
Run `main.py` located in the `src` directory

## Docker
The bot can also be run using Docker. \
A prebuilt image is available on [Docker Hub](https://hub.docker.com/r/jonas0092/free-epicgames-bot). \
Alternatively, you can build the image by yourself using the provided Dockerfile as follows: \
`docker build -t <image-name> .` \
You can run the image with this command: \
`docker run -e BOT_TOKEN=<bot-token> -e CHANNEL_ID=<channel-id> --name <container-name> -t <image-name>`
where `<image-name>` is `jonas0092/free-epicgames-bot` or the name you specified
