from bol_kalaha.kalaha_game import KalahaGame

class KalahaManager:
    game = KalahaGame(number_of_pits=6, starting_balls=6)

    def new_game(
        self, number_of_pits: int, starting_balls: int, default_game_mode: bool
    ):
        self.game = KalahaGame(
            number_of_pits=number_of_pits,
            starting_balls=starting_balls,
            default_game_mode=default_game_mode,
        )

    def play_pit(self, pit_index: int) -> dict:
        self.game.play_pit(pit_index)
        return self.get_scores()

    def get_scores(self) -> dict:
        return self.game.get_score_dict()
