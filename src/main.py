from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.api_model import PitList, Scores
from src.kalaha_enums import GameType
from src.kalaha_errors import NotPlayableError
from src.kalaha_game_manager import KalahaManager

app = FastAPI()
manager = KalahaManager()


class NewGameData(BaseModel):
    starting_balls: int
    number_of_pits: int
    game_type: GameType


class PlayPitData(BaseModel):
    selected_pit: int


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse("/docs")


@app.get("/get_scores")
def get_scores() -> Scores:
    return Scores.model_validate(manager.get_scores())


@app.get("/get_all_pits")
def get_all_pits() -> PitList:
    return PitList.model_validate(manager.get_all_pits())


@app.put("/new_game")
def new_game(new_game_data: NewGameData):
    manager.new_game(
        starting_balls=new_game_data.starting_balls,
        number_of_pits=new_game_data.number_of_pits,
        game_type=new_game_data.game_type,
    )
    return_dict = {
        "message": f"started a new game!, number of balls: {new_game_data.starting_balls}"
        f", number of pits: {new_game_data.number_of_pits}"
        f", default game mode {new_game_data.game_type}"
    }
    scores = manager.get_scores()
    return_dict.update(scores)
    return return_dict


@app.put("/play_pit")
def play_pit(play_pit_data: PlayPitData):
    return_dict = {}
    try:
        manager.play_pit(play_pit_data.selected_pit)
    except NotPlayableError as val_exc:
        raise HTTPException(status_code=400, detail=str(val_exc))

    scores = manager.get_scores()
    return_dict.update(scores)
    return return_dict
