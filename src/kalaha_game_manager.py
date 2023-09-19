from src.kalaha_enums import GameType
from src.kalaha_game import KalahaGame


class KalahaManager:
    game = KalahaGame(number_of_pits=6, starting_balls=6)

    def new_game(self, number_of_pits: int, starting_balls: int, game_type: GameType) -> None:
        self.game = KalahaGame(
            number_of_pits=number_of_pits,
            starting_balls=starting_balls,
            game_type=game_type,
        )

    def play_pit(self, pit_index: int) -> dict:
        self.game.play_pit(pit_index)
        return self.get_scores()

    def get_scores(self) -> dict:
        return self.game.get_score_dict()

    def get_all_pits(self) -> dict:
        return self.game.get_all_pits_dict()