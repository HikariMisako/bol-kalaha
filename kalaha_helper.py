from ball_pit import BallPit


def create_player_pits(
    number_playing_pits: int, associated_player_is_first: bool, starting_balls: int
) -> list[BallPit]:
    # we need to create regular pits for each player, plus a scoring pit for each
    pit_list = [
        BallPit(associated_player_is_first, pit_type="small", ball_count=starting_balls)
        for _i in range(number_playing_pits)
    ]
    pit_list.append(BallPit(associated_player_is_first, pit_type="large"))
    return pit_list


def create_score_overview(current_player: bool, all_pits: list[BallPit], game_is_done: [bool, str]) -> dict:
    """
    :return: Returns a dictionary containing a human-readable game state with:
    - Current number of balls for each pit
    - A line for each player in the kalaha "board" format
    - Whose turn it is
    """
    return_dict = {
        # the pit index is useful for play, so we add both the index and the short string to the output
        "pits": "  ".join(
            [f"{i}:{all_pits[i].short_str()}" for i in range(len(all_pits))]
        )
    }

    player_a_pits = [pit for pit in all_pits if pit.match_player(True)]
    player_b_pits = [pit for pit in all_pits if pit.match_player(False)]

    player_b_line = "  ".join(
        [str(pit.get_ball_count()) for pit in player_b_pits][::-1]
    )
    player_a_line = "   " + "  ".join(
        [str(pit.get_ball_count()) for pit in player_a_pits]
    )
    return_dict["player_2"] = player_b_line
    return_dict["player_1"] = player_a_line

    if current_player:
        return_dict["turn"] = "Current player: FIRST PLAYER"
    else:
        return_dict["turn"] = "Current player: SECOND PLAYER"

    if game_is_done:
        return_dict["game_outcome"] = game_is_done
    return return_dict
