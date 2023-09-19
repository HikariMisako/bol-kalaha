from bol_kalaha.ball_pit import BallPit
from bol_kalaha.kalaha_helper import create_player_pits, create_score_overview


class KalahaGame:
    pit_list: list = []
    current_player_is_first: [bool, str] = True
    game_is_done: [bool, str] = False
    # some articles state that _any_ time a player lands on his own pit he gets another turn
    # while not a specific requirement, it's common enough to implement
    # in the default mode this does not happen
    default_game_mode: bool

    def __init__(self, number_of_pits: int, starting_balls: int, default_game_mode: bool = True):
        player_a_pits = create_player_pits(
            number_playing_pits=number_of_pits,
            associated_player_is_first=True,
            starting_balls=starting_balls,
        )
        player_b_pits = create_player_pits(
            number_playing_pits=number_of_pits,
            associated_player_is_first=False,
            starting_balls=starting_balls,
        )
        self.pit_list = player_a_pits + player_b_pits
        self.default_game_mode = default_game_mode

    def get_player_pits(self, player_is_first: bool) -> list[BallPit]:
        return [pit for pit in self.pit_list if pit.match_player(player_is_first)]

    def get_scoring_pit(self, player: bool) -> BallPit:
        # there is only one scoring pit per player, so filtering is easy
        return [pit for pit in self.get_player_pits(player) if pit.is_large()][0]

    def get_regular_pits(self, player_is_first: bool) -> list[BallPit]:
        return [pit for pit in self.get_player_pits(player_is_first) if pit.is_small()]

    def get_player_balls_remaining(self, player: bool) -> int:
        """
        Count the number of balls the player can play
        :param player: what player to check
        :return: number of balls that is playable
        """
        regular_player_pits = self.get_regular_pits(player)
        playable_balls_count = sum(
            [pit.get_ball_count() for pit in regular_player_pits]
        )
        return playable_balls_count

    def get_player_score(self, player_is_first: bool) -> int:
        return self.get_scoring_pit(player_is_first).get_ball_count()

    def get_score_dict(self) -> dict:
        return create_score_overview(
            current_player=self.current_player_is_first,
            all_pits=self.pit_list,
            game_is_done=self.game_is_done,
        )

    def _switch_player(self) -> None:
        self.current_player_is_first = not self.current_player_is_first

    def get_current_player(self) -> bool:
        return self.current_player_is_first

    def check_endgame(self) -> [bool, str]:
        """
        If either of the players has no more balls to play, the game is over
        :return: return the winner as a string if the game is over.
        """
        if (
            self.get_player_balls_remaining(player=True) == 0
            or self.get_player_balls_remaining(player=False) == 0
        ):
            self.current_player_is_first = None
            if self.get_player_score(player_is_first=True) > self.get_player_score(player_is_first=False):
                self.game_is_done = "Player one wins!"
            elif self.get_player_score(player_is_first=True) < self.get_player_score(player_is_first=False):
                self.game_is_done = "Player two wins!"
            else:
                # According to wikipedia, a draw is possible
                self.game_is_done = "DRAW!?, NOBODY WINS?"
        return self.game_is_done

    def get_opposite_pit(self, pit_index: int) -> BallPit:
        """
        Used for the case when a player ends up in his own pit that was empty before
        We don't need to grab the opposite scoring pit, but it's a nice bonus if we can
        :param pit_index:
        :return: the pit 'opposite' to the index given as input.
        """
        if self.pit_list[pit_index].is_small():
            # length of list minus selected index would return the 'opposite' of a list normally
            # however, we have 2 scoring pits that need to be ignored, hence we need a -2 in there
            return self.pit_list[len(self.pit_list) - 2 - pit_index]
        else:
            # either the scoring pit is the last pit (and thus belongs to the second player)
            # or the scoring pit belongs to the first player
            if pit_index == len(self.pit_list) - 1:
                return self.get_scoring_pit(True)
            else:
                return self.pit_list[len(self.pit_list) - 1]

    def _distribute_balls_from_pit(self, start_index: int) -> int:
        """
        Take the balls from one pit, and distribute them through the following pits
        :param start_index: Index of selected starting pit
        :return: index of the pit where the last ball ended up in
        """
        played_pit = self.pit_list[start_index]
        current_pit_index = start_index
        number_of_balls_played = played_pit.empty_pit()
        while number_of_balls_played > 0:
            current_pit_index += 1
            # check if we've gone round a loop
            if current_pit_index > len(self.pit_list) - 1:
                current_pit_index = 0

            current_pit = self.pit_list[current_pit_index]
            if (
                current_pit.is_large()
                and current_pit.match_player(self.get_current_player())
            ) or current_pit.is_small():
                current_pit.add_ball()
                number_of_balls_played -= 1
        return current_pit_index

    def _determine_turn_end(self, ended_pit_index) -> None:
        """
        Perform the turn end logic:
        if it's their big pit they get another turn
        if it's their small pit and that small pit _was_ empty
        they take all balls from the opposite pit and their own
        :param ended_pit_index: at which pit was the last ball played?
        :return: None
        """
        ended_pit = self.pit_list[ended_pit_index]
        if ended_pit.match_player(self.get_current_player()):
            if ended_pit.is_small():
                # when the alternative game mode is active,
                # the player _always_ gets another turn when landing on their own pit
                # in the default, only when the pit was empty before landing on it
                if ended_pit.get_ball_count() == 1:
                    opposite_pit = self.get_opposite_pit(ended_pit_index)
                    scored_balls = opposite_pit.empty_pit() + ended_pit.empty_pit()
                    self.get_scoring_pit(self.get_current_player()).add_ball(
                        ball_count=scored_balls
                    )
                if self.default_game_mode:
                    self._switch_player()
            # no need for the else case where the ending pit is large, just don't switch the player
        else:
            self._switch_player()

    def play_pit(self, pit_index: int) -> None:
        """
        Play the pit at the index given
        :param pit_index: index of the pit to play
        :return: None
        """
        if pit_index < 0:
            raise ValueError("Positive pit indices only!")
        if self.game_is_done:
            raise ValueError("Game is over, no more moves can be made!")
        current_player = self.get_current_player()
        played_pit = self.pit_list[pit_index]
        played_pit.is_playable(current_player)
        ended_pit_index = self._distribute_balls_from_pit(pit_index)
        self._determine_turn_end(ended_pit_index)
        self.check_endgame()


if __name__ == '__main__':
    import random
    finished_game = KalahaGame(number_of_pits=6, starting_balls=6,default_game_mode=False)
    while finished_game.get_current_player() is not None:
        try_pit = random.randint(0, 6 * 2 + 1)
        try:
            finished_game.play_pit(try_pit)
            print(finished_game.get_score_dict())
        except ValueError as _exc:
            pass