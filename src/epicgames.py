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
