import random

from ball_pit import BallPit


def create_player_pits(
    number_playing_pits: int, associated_player_is_first: bool, starting_balls: int
):
    # we need to create regular pits for each player, plus a scoring pit for each
    pit_list = [
        BallPit(associated_player_is_first, pit_type="small", ball_count=starting_balls)
        for _i in range(number_playing_pits)
    ]
    pit_list.append(BallPit(associated_player_is_first, pit_type="large"))
    return pit_list


class KalahaGame:
    pit_list = []
    current_player_is_first = True
    number_of_pits = 0
    game_is_done = False

    def __init__(self, number_of_pits: int, starting_balls: int):
        self.pit_list = create_player_pits(
            number_playing_pits=number_of_pits,
            associated_player_is_first=True,
            starting_balls=starting_balls,
        )
        self.pit_list.extend(
            create_player_pits(
                number_playing_pits=number_of_pits,
                associated_player_is_first=False,
                starting_balls=starting_balls,
            )
        )
        self.number_of_pits = number_of_pits

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

    def switch_player(self) -> None:
        self.current_player_is_first = not self.current_player_is_first

    def get_current_player(self) -> bool:
        return self.current_player_is_first

    def check_endgame(self) -> [bool, str]:
        """
        If either of the players has no more balls to play, the game is over
        :return: return True if the game is over.
        """
        if (
            self.get_player_balls_remaining(True) == 0
            or self.get_player_balls_remaining(False) == 0
        ):
            self.current_player_is_first = None
            self.game_is_done = True
            if self.get_player_score(True) > self.get_player_score(False):
                return "Player one wins!"
            elif self.get_player_score(True) < self.get_player_score(False):
                return "Player two wins!"
            else:
                return "DRAW!?"
        return False

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

    def get_score_dict(self) -> dict:
        """
        :return: Returns a dictionary containing a human-readable game state with:
        - Current number of balls for each pit
        - A line for each player in the kalaha "board" format
        - Whose turn it is
        """
        return_dict = {
            # the pit index is useful for play, so we add both the index and the short string to the output
            "pits": "  ".join(
                [
                    f"{i}:{self.pit_list[i].short_str()}"
                    for i in range(len(self.pit_list))
                ]
            )
        }

        player_a_pits = self.get_player_pits(player_is_first=True)
        player_b_pits = self.get_player_pits(player_is_first=False)

        player_b_line = "  ".join(
            [str(pit.get_ball_count()) for pit in player_b_pits][::-1]
        )
        player_a_line = "   " + "  ".join(
            [str(pit.get_ball_count()) for pit in player_a_pits]
        )
        return_dict["player_2"] = player_b_line
        return_dict["player_1"] = player_a_line

        if self.current_player_is_first:
            return_dict["turn"] = "Current player: FIRST PLAYER"
        else:
            return_dict["turn"] = "Current player: SECOND PLAYER"
        return return_dict

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
                if ended_pit.get_ball_count() == 1:
                    opposite_pit = self.get_opposite_pit(ended_pit_index)
                    scored_balls = opposite_pit.empty_pit() + ended_pit.empty_pit()
                    self.get_scoring_pit(self.get_current_player()).add_ball(
                        ball_count=scored_balls
                    )
                self.switch_player()
            # no need for the else case where the ending pit is large, just don't switch the player
        else:
            self.switch_player()

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
