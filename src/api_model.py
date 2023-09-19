from pydantic import BaseModel


class Scores(BaseModel):
    scores_list: list[str]
    game_outcome: str
    player_turn: str
