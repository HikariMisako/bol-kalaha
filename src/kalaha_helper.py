from src.ball_pit import BallPit
from src.kalaha_enums import PitType, Player


def create_player_pits(
    number_playing_pits: int, associated_player: Player, starting_balls: int
) -> list[BallPit]:
    # we need to create regular pits for each player, plus a scoring pit for each
    pit_list = [
        BallPit(
            associated_player=associated_player,
            pit_type=PitType.SMALL,
            ball_count=starting_balls,
        )
        for _i in range(number_playing_pits)
    ]
    pit_list.append(
        BallPit(associated_player=associated_player, pit_type=PitType.LARGE)
    )
    return pit_list


def create_score_overview(
    current_player: Player, all_pits: list[BallPit], game_is_done: [bool, str]
) -> dict:
    """
    :return: Returns a dictionary containing a human-readable game state with:
    - Current number of balls for each pit
    - A line for each player in the kalaha "board" format, sideways!
        - Displaying for each pit, the index and the number of balls
    - Whose turn it is

    Display is sideways, with player 1 on the left and player 2 on the right.
    Example with 2 pits and 2 balls starting:
    "00": "I:      P1     P2     :I",
    "01": "LARGE>         0      :05",
    "02": "00:     2      2      :04",
    "03": "01:     2      2      :03",
    "04": "02:     0      <LARGE",
    """
    # this format is far from ideal, however once a proper display format is decided this can be reworked
    # ideally, this function is discarded and the manager function get_all_pits is used for the user interface
    lines = ["I:      P1     P2     :I"]

    # for each pit in the list, we want to display the index and the current number of balls.
    for i in range(int(len(all_pits) / 2)):
        mirror_i = len(all_pits) - i - 2
        p1_pit = all_pits[i]
        p2_pit = all_pits[mirror_i]
        # first 2 lines are an exception
        if i == 0:
            lines.append(
                f"LARGE>         {all_pits[mirror_i + 1].get_ball_count()}      :{mirror_i + 1:02}"
            )
            lines.append(
                f"{i:02}:     {p1_pit.get_ball_count()}      {p2_pit.get_ball_count()}      :{mirror_i:02}"
            )
        elif p1_pit.is_large():
            lines.append(f"{i:02}:     {p1_pit.get_ball_count()}      <LARGE")
        else:
            lines.append(
                f"{i:02}:     {p1_pit.get_ball_count()}      {p2_pit.get_ball_count()}      :{mirror_i:02}"
            )

    return_dict = {
        "scores_list": lines,
        "player_turn": f"Current player: {current_player}",
    }

    if game_is_done:
        return_dict["game_outcome"] = game_is_done
    else:
        return_dict["game_outcome"] = "Game is ongoing!"
    return return_dict
