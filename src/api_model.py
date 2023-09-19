from pydantic import BaseModel

from src.ball_pit import BallPit


class Scores(BaseModel):
    scores_list: list[str]
    game_outcome: str
    player_turn: str


class PitList(BaseModel):
    pit_list: list[BallPit]
