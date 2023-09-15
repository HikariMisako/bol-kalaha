from fastapi import FastAPI
from kalaha_game_manager import KalahaManager

app = FastAPI()
manager = KalahaManager()


def tabs_to_spaces(input_str: str) -> str:
    return input_str.replace("\t", "  ")


@app.get("/")
def get_scores():
    scores = manager.get_scores()
    return {
        "pits": tabs_to_spaces(scores[0]),
        "player_2": tabs_to_spaces(scores[1]),
        "player_1": " " + tabs_to_spaces(scores[2]),
        "turn": tabs_to_spaces(scores[3]),
    }


@app.put("/")
def new_game(starting_balls: int, number_of_pits: int):
    manager.new_game(starting_balls=starting_balls, number_of_pits=number_of_pits)
    return {"message": "started a new game!"}


@app.post("/")
def play_pit(selected_pit: int):
    try:
        manager.play_pit(selected_pit)
    except ValueError as val_exc:
        return {"error": str(val_exc)}

    scores = manager.get_scores()
    return {
        "pits": tabs_to_spaces(scores[0]),
        "player_2": tabs_to_spaces(scores[1]),
        "player_1": " " + tabs_to_spaces(scores[2]),
        "turn": tabs_to_spaces(scores[3]),
    }
