from ball_pit import BallPit

player_pits = 6


def create_player_pits(number_playing_pits: int, associated_player: str):
    # we need to create the regular pits for each player, plus a scoring pit for each
    pit_list = [BallPit(associated_player, pit_type="small") for _i in range(number_playing_pits)]
    pit_list.append(BallPit(associated_player, pit_type="large"))
    return pit_list


class KalahaGame:
    pit_list = []

    def __init__(self, number_of_pits: int = player_pits):
        self.pit_list.extend(create_player_pits(number_playing_pits=number_of_pits, associated_player="A"))
        self.pit_list.extend(create_player_pits(number_playing_pits=number_of_pits, associated_player="B"))

    def play_pit(self, pit_index: int, players_turn: str):
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
