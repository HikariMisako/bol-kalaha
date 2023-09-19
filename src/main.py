from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from src.api_model import Scores
from src.kalaha_errors import NotPlayableError
from src.kalaha_game_manager import KalahaManager
from src.kalaha_enums import GameType

app = FastAPI()
manager = KalahaManager()


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("/docs")


@app.get("/get_scores")
def get_scores() -> Scores:
    return Scores.model_validate(manager.get_scores())


@app.put("/new_game")
def new_game(starting_balls: int, number_of_pits: int, game_type: GameType):
    manager.new_game(
        starting_balls=starting_balls,
        number_of_pits=number_of_pits,
        game_type=game_type,
    )
    return_dict = {
        "message": f"started a new game!, number of balls: {starting_balls}"
        f", number of pits: {number_of_pits}"
        f", default game mode {game_type}"
    }
    scores = manager.get_scores()
    return_dict.update(scores)
    return return_dict


@app.put("/play_pit")
def play_pit(selected_pit: int):
    return_dict = {}
    try:
        manager.play_pit(selected_pit)
    except NotPlayableError as val_exc:
        raise HTTPException(status_code=409, detail=str(val_exc))

    scores = manager.get_scores()
    return_dict.update(scores)
    return return_dict
