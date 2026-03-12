import os

from epicstore_api import EpicGamesStoreAPI


def get_free_games() -> list[dict]:
    """
    :return: A list of the games that are currently free on Epic Games
    """
    api: EpicGamesStoreAPI = EpicGamesStoreAPI()
    data: dict = api.get_free_games()
    games: list[dict] = data["data"]["Catalog"]["searchStore"]["elements"]
    free_games: list[dict] = []

    for game in games:
        if game["price"]["totalPrice"]["discountPrice"] == 0:
            free_games.append(game)

    return free_games


def get_new_free_games() -> list[dict]:
    """
    Retrieve the games that are currently free on Epic Games and check whether they are new.
    'New' meaning that they were not free when this function had last been called.
    :return: A list of the new games that are currently free on Epic Games
    """
    if os.path.exists("free_games.txt"):
        with open("free_games.txt", "r") as f:
            old_free_game_titles: list[str] = f.read().splitlines()
    else:
        old_free_game_titles = []

    current_free_games: list[dict] = get_free_games()
    new_free_games: list[dict] = []

    for game in current_free_games:
        if game["title"] not in old_free_game_titles:
            new_free_games.append(game)

    _save_free_games(current_free_games)

    return new_free_games


def _save_free_games(games: list[dict]) -> None:
    """
    Save a list of titles of games to a file
    """
    text: str = ""
    for game in games:
        text += f"{game['title']}\n"

    with open("free_games.txt", "w") as f:
        f.write(text.strip())
