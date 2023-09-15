from kalaha_game import KalahaGame


class KalahaManager:
    game = KalahaGame(number_of_pits=6, starting_balls=6)

    def new_game(self, number_of_pits: int, starting_balls: int):
        self.game = KalahaGame(
            number_of_pits=number_of_pits, starting_balls=starting_balls
        )

    def play_pit(self, pit_index: int):
        try:
            self.game.play_pit(pit_index)
        except ValueError as val_exc:
            return str(val_exc)
        return self.get_scores()

    def get_scores(self):
        return self.game.get_score_text()
