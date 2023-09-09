from ball_pit import BallPit

player_pits = 6


def create_player_pits(number_playing_pits: int, associated_player_is_first: bool):
    # we need to create the regular pits for each player, plus a scoring pit for each
    pit_list = [BallPit(associated_player_is_first, pit_type="small") for _i in range(number_playing_pits)]
    pit_list.append(BallPit(associated_player_is_first, pit_type="large"))
    return pit_list


class KalahaGame:
    pit_list = []
    current_player_is_first = True
    number_of_pits = 0

    def __init__(self, number_of_pits: int = player_pits):
        self.pit_list.extend(create_player_pits(number_playing_pits=number_of_pits, associated_player_is_first=True))
        self.pit_list.extend(create_player_pits(number_playing_pits=number_of_pits, associated_player_is_first=False))
        self.number_of_pits = number_of_pits

    def get_scoring_pit(self, player_is_first: bool):
        # there is only one scoring pit per player, so filtering is easy
        return [pit for pit in self.pit_list if pit.match_player(player_is_first) and not pit.is_small()][0]

    def get_opposite_pit(self, pit_index: int):
        # the selection of the opposite pit works only for small pits
        # the scoring pits are an exception, and the opposite is never needed
        if self.pit_list[pit_index].is_small():
            return self.pit_list[len(self.pit_list) - 2 - pit_index]
        else:
            raise TypeError("Opposite pit selection is currently not supported")

    def play_pit(self, pit_index: int, players_turn: bool):
        played_pit = self.pit_list[pit_index]
        if not played_pit.match_player(players_turn):
            raise ValueError("This pit does not belong to this player!")
        if played_pit.get_ball_count <= 0:
            raise ValueError("This pit is empty and cannot be played!")

        num_balls_played = played_pit.empty_pit()
        # remember this can go round and round!
        # and, the played pit gets emptied first, then move on to the next pit so + 1
        ## final_pit_index = pit_index + num_balls_played + 1

        # let's loop first, see if we can list comprehend later?
        current_pit_index = pit_index
        while num_balls_played > 0:
            current_pit_index += 1
            # check if we've gone round a loop
            if current_pit_index > len(self.pit_list):
                current_pit_index = 0

            current_pit = self.pit_list[current_pit_index]
            if current_pit.match_player(players_turn):
                current_pit.add_ball()
                num_balls_played -= 1

        # here we find out what the last played pit is
        ended_pit = self.pit_list[current_pit_index]
        # there's some logic to be had if the last pit is the players own
        # then, if it's their big pit they get another turn
        # if it's their small pit, they take all balls from the opposite pit
        if ended_pit.match_player(self.current_player_is_first):
            if ended_pit.is_small() and ended_pit.get_ball_count() == 1:
                opposite_pit = self.get_opposite_pit(current_pit_index)
                scored_balls = opposite_pit.empty()
                self.get_scoring_pit(players_turn).add_ball(ball_count=scored_balls)
            # no need for the else case where the ending pit is large
        else:
            self.current_player_is_first = not self.current_player_is_first
