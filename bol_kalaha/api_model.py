from pydantic import BaseModel


class Scores(BaseModel):
    player_turn: str
    game_outcome: str
    scores_list: list[str]
    error_status: str
