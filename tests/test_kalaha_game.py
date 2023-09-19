import random

from pytest import fixture, raises
from src.kalaha_enums import Player
from src.kalaha_errors import NotPlayableError
from src.kalaha_game import KalahaGame
from src.kalaha_helper import create_score_overview

number_of_pits = 6
starting_balls = 6


@fixture
def clean_game():
    clean_game = KalahaGame(
        number_of_pits=number_of_pits, starting_balls=starting_balls
    )
    return clean_game


@fixture
def halfway_game():
    half_game = KalahaGame(number_of_pits=number_of_pits, starting_balls=starting_balls)
    for number in [2, 7, 3, 9, 0, 7, 1, 12, 5, 12, 9, 3, 5, 2, 10]:
        half_game.play_pit(number)
    # halfway pits, index:score
    # P0:3	P1:3	P2:1	P3:2	P4:14	P5:2	P6:8	P7:5	P8:14	P9:0	P10:0	P11:11	P12:1	P13:8
    # first player turn
    return half_game


@fixture
def finished_game():
    finished_game = KalahaGame(number_of_pits=6, starting_balls=6)
    while finished_game.get_current_player() is not None:
        try_pit = random.randint(0, number_of_pits * 2 + 1)
        try:
            finished_game.play_pit(try_pit)
        except ValueError as _exc:
            pass
    return finished_game


def test_get_specific_player_pits(clean_game, halfway_game):
    # given a clean or halfway game
    clean_pits_a = clean_game.get_player_pits(Player.PLAYER_1)
    used_pits_a = halfway_game.get_player_pits(Player.PLAYER_2)
    # when the player-specific pits from a clean or halfway game are grabbed
    for pit in clean_pits_a:
        assert pit.match_player(Player.PLAYER_1)
    for pit in used_pits_a:
        assert pit.match_player(Player.PLAYER_2)
    # then, the pits should match the players from the selection


def test_get_clean_scoring_pit(clean_game):
    # given a clean game
    # when the scoring pit for a player is selected
    clean_scoring_pit_a = clean_game.get_scoring_pit(Player.PLAYER_1)
    # then there should be 0 balls in the scoring pit
    # and the scoring pit should match the player
    # and the scoring pit should not be playable
    assert clean_scoring_pit_a.get_ball_count() == 0
    assert clean_scoring_pit_a.match_player(Player.PLAYER_1)
    with raises(ValueError):
        clean_scoring_pit_a.is_playable(Player.PLAYER_1)


def test_get_finished_scoring_pit(finished_game):
    # given a finished game
    # when the scoring pit for a player is selected
    finished_scoring_pit_a = finished_game.get_scoring_pit(Player.PLAYER_1)
    # then there should be more than 0 balls in the scoring pit
    # and the scoring pit should match the player
    # and the scoring pit should not be playable
    assert finished_scoring_pit_a.get_ball_count() > 0
    assert finished_scoring_pit_a.match_player(Player.PLAYER_1)
    with raises(ValueError):
        finished_scoring_pit_a.is_playable(Player.PLAYER_1)


def test_get_regular_pits(clean_game):
    # given a clean game
    # when the playing pits for a player are selected
    regular_pits_player_1 = clean_game.get_regular_pits(Player.PLAYER_1)
    regular_pits_player_2 = clean_game.get_regular_pits(Player.PLAYER_2)
    # then the number of pits should match the starting number of pits
    # and the number of balls in the pits should match
    # and only small pits should have been grabbed
    assert len(regular_pits_player_1) == number_of_pits
    assert len(regular_pits_player_2) == number_of_pits
    for pit in clean_game.get_regular_pits(Player.PLAYER_1):
        assert pit.get_ball_count() == starting_balls
        assert pit.is_small()


def test_get_player_balls_remaining_clean(clean_game, halfway_game):
    # given a clean game
    # when the number of playable balls is checked, it should be the same as the number of pits & starting balls
    assert (
        clean_game.get_player_balls_remaining(Player.PLAYER_1)
        == number_of_pits * starting_balls
    )
    # then, when a halfway game is checked, the number of available balls should be lower!
    assert (
        halfway_game.get_player_balls_remaining(Player.PLAYER_1)
        < number_of_pits * starting_balls
    )


def test_get_player_score(clean_game):
    # given a clean game
    # when the score for a player is assessed
    clean_game_score_p1 = clean_game.get_player_score(Player.PLAYER_1)
    clean_game_score_p2 = clean_game.get_player_score(Player.PLAYER_2)
    # then this value should be zero
    assert clean_game_score_p1 == 0
    assert clean_game_score_p2 == 0


def test_get_player_score_finished(finished_game):
    # given a finished game
    # when the score for a player is assessed
    finished_score = finished_game.get_player_score(Player.PLAYER_1)
    # then the score should be above 0!
    assert finished_score > 0


def test_switch_player(clean_game):
    # given a clean game
    # when the player is switched multiple times
    assert clean_game.get_current_player() == Player.PLAYER_1
    clean_game._switch_player()
    assert clean_game.get_current_player() == Player.PLAYER_2
    clean_game._switch_player()
    assert clean_game.get_current_player() == Player.PLAYER_1
    # then the player should be swapped around every time


def test_check_endgame(clean_game, halfway_game, finished_game):
    # given a clean game, halfway game and a finished game
    # when endgame is checked, this should match the game state
    assert not clean_game.check_endgame()
    assert not halfway_game.check_endgame()
    assert finished_game.check_endgame()
    assert isinstance(finished_game.check_endgame(), str)

    # then, the finished game should have a winner declared in the "game_outcome"
    finished_score_overview = create_score_overview(
        finished_game.get_current_player(),
        finished_game.pit_list,
        finished_game.game_is_done,
    )
    assert "game_outcome" in finished_score_overview


def test_get_opposite_pit():
    # given a game with indices set as ball counts
    # in order to simply test the base case of 6 pits set them manually
    # starting balls cannot be 0 so add a ball to the comparison everywhere
    game = KalahaGame(number_of_pits=6, starting_balls=1)
    # get_opposite pit returns the pit itself, not the index,
    # by adding the same amount of balls as the index we can check the numbers anyway
    for i in range(1, 14):
        game.pit_list[i].add_ball(i)
    # when opposite pits are selected the values should match as described
    # opposite of 0 should be 12
    assert game.get_opposite_pit(0).get_ball_count() == 12 + 1
    # opposite of 4 should be 8
    assert game.get_opposite_pit(4).get_ball_count() == 8 + 1
    # opposite of 7 should be 5
    assert game.get_opposite_pit(7).get_ball_count() == 5 + 1
    # opposite of 10 should be 2
    assert game.get_opposite_pit(10).get_ball_count() == 2 + 1


def test_play_pit(halfway_game, finished_game):
    # given a halfway game, first player's turn
    # P0:3	P1:3	P2:1	P3:2	P4:14	P5:2	P6:8	P7:5	P8:14	P9:0	P10:0	P11:11	P12:1	P13:8
    # when a bunch of pits are played
    assert halfway_game.pit_list[0].get_ball_count() == 3
    halfway_game.play_pit(0)
    assert halfway_game.pit_list[0].get_ball_count() == 0
    assert halfway_game.pit_list[1].get_ball_count() == 4
    assert halfway_game.pit_list[2].get_ball_count() == 2
    assert halfway_game.pit_list[3].get_ball_count() == 3
    assert halfway_game.get_current_player() == Player.PLAYER_2
    # then the current player should be player 2
