from ball_pit import BallPit
import random
# player_pits = 6
# starting_balls = 6


def create_player_pits(number_playing_pits: int, associated_player_is_first: bool, starting_balls: int):
    # we need to create the regular pits for each player, plus a scoring pit for each
    pit_list = [BallPit(associated_player_is_first, pit_type="small") for _i in range(number_playing_pits)]
    for pit in pit_list:
        pit.add_ball(ball_count=starting_balls)
    pit_list.append(BallPit(associated_player_is_first, pit_type="large"))
    return pit_list


class KalahaGame:
    pit_list = []
    current_player_is_first = True
    number_of_pits = 0

    def __init__(self, number_of_pits: int, starting_balls: int):
        self.pit_list.extend(create_player_pits(
            number_playing_pits=number_of_pits,
            associated_player_is_first=True,
            starting_balls=starting_balls
        ))
        self.pit_list.extend(create_player_pits(
            number_playing_pits=number_of_pits,
            associated_player_is_first=False,
            starting_balls=starting_balls
        ))
        self.number_of_pits = number_of_pits

    def get_player_pits(self, player_is_first: bool):
        return [pit for pit in self.pit_list if pit.match_player(player_is_first)]

    def get_scoring_pit(self, player_is_first: bool):
        # there is only one scoring pit per player, so filtering is easy
        return [pit for pit in self.get_player_pits(player_is_first) if pit.is_large()][0]

    def get_regular_pits(self, player_is_first: bool):
        return [pit for pit in self.get_player_pits(player_is_first) if pit.is_small()]

    def player_balls_remaining(self, player_is_first: bool):
        regular_player_pits = self.get_regular_pits(player_is_first)
        playable_balls_count = sum([pit.get_ball_count() for pit in regular_player_pits])
        return playable_balls_count

    def check_endgame(self):
        if self.player_balls_remaining(True) == 0 or self.player_balls_remaining(False) == 0:
            self.current_player_is_first = None
            self.print_scores()
            print("Game over!")
            if self.get_player_score(True) > self.get_player_score(False):
                print("Player one wins!")
            elif self.get_player_score(True) < self.get_player_score(False):
                print("Player two wins!")
            else:
                print("Nobody won!?")
        return False

    def get_opposite_pit(self, pit_index: int):
        # the selection of the opposite pit works only for small pits
        # the scoring pits are an exception, and the opposite is never needed
        if self.pit_list[pit_index].is_small():
            return self.pit_list[len(self.pit_list) - 2 - pit_index]
        else:
            # TODO just grab the other scoring pit
            raise TypeError("Opposite pit selection is currently not supported")

    def print_scores(self):
        print("\t".join([f"P{i}:{self.pit_list[i].get_ball_count()}" for i in range(len(self.pit_list))]))

        player_a_pits = self.get_player_pits(player_is_first=True)
        player_b_pits = self.get_player_pits(player_is_first=False)

        player_b_printline = "\t".join([str(pit.get_ball_count()) for pit in player_b_pits][::-1])
        player_a_printline = "\t" + "\t".join([str(pit.get_ball_count()) for pit in player_a_pits])
        print(player_b_printline)
        print(player_a_printline)

        if self.current_player_is_first:
            print("Current player: FIRST PLAYER")
        else:
            print("Current Player: SECOND PLAYER")

    def get_player_score(self, player_is_first: bool):
        return self.get_scoring_pit(player_is_first).get_ball_count()

    def switch_player(self):
        self.current_player_is_first = not self.current_player_is_first

    def play_pit(self, pit_index: int):
        played_pit = self.pit_list[pit_index]
        if not played_pit.match_player(self.current_player_is_first):
            raise ValueError("This pit does not belong to this player!")
        if played_pit.get_ball_count() <= 0:
            raise ValueError("This pit is empty and cannot be played!")

        num_balls_played = played_pit.empty_pit()
        # remember this can go round and round!
        current_pit_index = pit_index
        while num_balls_played > 0:
            current_pit_index += 1
            # check if we've gone round a loop
            if current_pit_index > len(self.pit_list) - 1:
                current_pit_index = 0

            current_pit = self.pit_list[current_pit_index]
            if current_pit.is_large() and current_pit.match_player(self.current_player_is_first):
                current_pit.add_ball()
                num_balls_played -= 1
            if current_pit.is_small():
                current_pit.add_ball()
                num_balls_played -= 1

        # here we find out what the last played pit is
        ended_pit = self.pit_list[current_pit_index]
        # there's some logic to be had if the last pit is the players own
        # then, if it's their big pit they get another turn
        # if it's their small pit, they take all balls from the opposite pit
        if ended_pit.match_player(self.current_player_is_first):
            if ended_pit.is_small():
                if ended_pit.get_ball_count() == 1:
                    opposite_pit = self.get_opposite_pit(current_pit_index)
                    scored_balls = opposite_pit.empty_pit() + ended_pit.empty_pit()
                    self.get_scoring_pit(self.current_player_is_first).add_ball(ball_count=scored_balls)
                self.switch_player()
            # no need for the else case where the ending pit is large
        else:
            self.switch_player()

        self.print_scores()
        self.check_endgame()


if __name__ == '__main__':
    game = KalahaGame(number_of_pits=6, starting_balls=6)
    for number in [2, 7, 3, 9, 0, 7, 1, 12, 5, 12, 9, 3, 5, 2, 10]:
        print(number)
        game.play_pit(number)
    while game.current_player_is_first is not None:
        try_pit = random.randint(0, 13)
        try:
            game.play_pit(try_pit)
        except:
            print(f"lmao cant play pit {try_pit}")
