from ball_pit import BallPit

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

    def get_scoring_pit(self, player_is_first: bool):
        # there is only one scoring pit per player, so filtering is easy
        return [pit for pit in self.pit_list if pit.match_player(player_is_first) and pit.is_large()][0]

    def get_opposite_pit(self, pit_index: int):
        # the selection of the opposite pit works only for small pits
        # the scoring pits are an exception, and the opposite is never needed
        if self.pit_list[pit_index].is_small():
            return self.pit_list[len(self.pit_list) - 2 - pit_index]
        else:
            raise TypeError("Opposite pit selection is currently not supported")

    def print_scores(self):
        for i in range(len(self.pit_list)):
            pit_text = "Pit"
            pit = self.pit_list[i]
            if pit.is_large():
                pit_text = "SCORE PIT"
            print(f"{pit_text} {i} score {self.pit_list[i].get_ball_count()}")
        if self.current_player_is_first:
            print("Current player: FIRST PLAYER")
        else:
            print("Current Player: SECOND PLAYER")

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

        # TODO you were here, debug this loop!
        # the last round of the loop adds one to current_pit_index so remove that here
        current_pit_index = current_pit_index - 1
        # here we find out what the last played pit is
        ended_pit = self.pit_list[current_pit_index]
        # there's some logic to be had if the last pit is the players own
        # then, if it's their big pit they get another turn
        # if it's their small pit, they take all balls from the opposite pit
        if ended_pit.match_player(self.current_player_is_first):
            if ended_pit.is_small() and ended_pit.get_ball_count() == 1:
                opposite_pit = self.get_opposite_pit(current_pit_index)
                scored_balls = opposite_pit.empty()
                self.get_scoring_pit(self.current_player_is_first).add_ball(ball_count=scored_balls)
            # no need for the else case where the ending pit is large
        else:
            self.current_player_is_first = not self.current_player_is_first

        self.print_scores()
        # TODO: check endgame



if __name__ == '__main__':
    game = KalahaGame(number_of_pits=6, starting_balls=6)
    game.play_pit(2)
    game.play_pit(7)
    game.play_pit(8)
    game.play_pit(0)
    print("done!")