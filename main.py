from fastapi import FastAPI

from kalaha_game_manager import KalahaManager

app = FastAPI()
manager = KalahaManager()


@app.get("/get_scores")
def get_scores():
    return manager.get_scores()


@app.put("/new_game")
def new_game(starting_balls: int, number_of_pits: int):
    manager.new_game(starting_balls=starting_balls, number_of_pits=number_of_pits)
    return {"message": "started a new game!"}


@app.put("/play_pit")
def play_pit(selected_pit: int):
    return_dict = {}
    try:
        manager.play_pit(selected_pit)
    except ValueError as val_exc:
        return_dict["ERROR"] = str(val_exc)

    scores = manager.get_scores()
    return_dict.update(scores)
    return return_dict
