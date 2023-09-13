import random

from kalaha_game import KalahaGame
from pytest import fixture, raises

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


def test_get_player_pits(clean_game, halfway_game):
    clean_pits_a = clean_game.get_player_pits(True)
    for pit in clean_pits_a:
        assert pit.match_player(True)
    used_pits_a = halfway_game.get_player_pits(True)
    for pit in used_pits_a:
        assert pit.match_player(True)


def test_get_scoring_pit(clean_game, halfway_game, finished_game):
    clean_scoring_pit_a = clean_game.get_scoring_pit(True)
    assert clean_scoring_pit_a.get_ball_count() == 0
    assert clean_scoring_pit_a.match_player(True)
    with raises(ValueError):
        clean_scoring_pit_a.is_playable(True)
    halfway_scoring_pit_a = halfway_game.get_scoring_pit(True)
    assert halfway_scoring_pit_a.get_ball_count() > 0
    assert halfway_scoring_pit_a.match_player(True)
    with raises(ValueError):
        halfway_scoring_pit_a.is_playable(True)
    finished_scoring_pit_a = finished_game.get_scoring_pit(True)
    assert finished_scoring_pit_a.get_ball_count() > 0
    assert finished_scoring_pit_a.match_player(True)
    with raises(ValueError):
        finished_scoring_pit_a.is_playable(True)


def test_get_regular_pits(clean_game):
    assert len(clean_game.get_regular_pits(True)) == number_of_pits
    assert len(clean_game.get_regular_pits(False)) == number_of_pits
    for pit in clean_game.get_regular_pits(True):
        assert pit.get_ball_count() == starting_balls
        assert pit.is_small()


def test_get_player_balls_remaining(clean_game, halfway_game, finished_game):
    assert (
        clean_game.get_player_balls_remaining(True) == number_of_pits * starting_balls
    )
    assert (
        halfway_game.get_player_balls_remaining(True) < number_of_pits * starting_balls
    )
    assert finished_game.get_player_balls_remaining(
        True
    ) < halfway_game.get_player_balls_remaining(True)


def test_get_player_score(clean_game, halfway_game, finished_game):
    # finished game is randomized, so making tests too specific might have random failures
    assert clean_game.get_player_score(True) == 0
    assert clean_game.get_player_score(False) == 0
    assert finished_game.get_player_score(True) > halfway_game.get_player_score(True)


def test_switch_player(clean_game):
    assert clean_game.get_current_player()
    clean_game.switch_player()
    assert not clean_game.get_current_player()
    clean_game.switch_player()
    assert clean_game.get_current_player()


def test_check_endgame(clean_game, halfway_game, finished_game):
    assert not clean_game.check_endgame()
    assert not halfway_game.check_endgame()
    assert finished_game.check_endgame()


def test_get_opposite_pit():
    # in order to simply test the base case of 6 pits set them manually
    # starting balls cannot be 0 so add a ball to the comparison everywhere
    game = KalahaGame(number_of_pits=6, starting_balls=1)
    # get_opposite pit returns the pit itself, not the index,
    # by adding the same amount of balls as the index we can check the numbers anyway
    for i in range(1, 14):
        game.pit_list[i].add_ball(i)
    # opposite of 0 should be 12
    assert game.get_opposite_pit(0).get_ball_count() == 12 + 1
    # opposite of 4 should be 8
    assert game.get_opposite_pit(4).get_ball_count() == 8 + 1
    # opposite of 7 should be 5
    assert game.get_opposite_pit(7).get_ball_count() == 5 + 1
    # opposite of 10 should be 2
    assert game.get_opposite_pit(10).get_ball_count() == 2 + 1


def test_play_pit(halfway_game, finished_game):
    # halfway game, first player's turn
    # P0:3	P1:3	P2:1	P3:2	P4:14	P5:2	P6:8	P7:5	P8:14	P9:0	P10:0	P11:11	P12:1	P13:8
    assert halfway_game.pit_list[0].get_ball_count() == 3
    halfway_game.play_pit(0)
    assert halfway_game.pit_list[0].get_ball_count() == 0
    assert halfway_game.pit_list[1].get_ball_count() == 4
    assert halfway_game.pit_list[2].get_ball_count() == 2
    assert halfway_game.pit_list[3].get_ball_count() == 3
    assert not halfway_game.get_current_player()

    with raises(ValueError):
        finished_game.play_pit(0)
