from kalaha_game import KalahaGame
from pytest import fixture, raises
import random


@fixture
def clean_game():
    clean_game = KalahaGame(number_of_pits=6, starting_balls=6)
    return clean_game


@fixture
def halfway_game():
    half_game = KalahaGame(number_of_pits=6, starting_balls=6)
    for number in [2, 7, 3, 9, 0, 7, 1, 12, 5, 12, 9, 3, 5, 2, 10]:
        print(number)
        half_game.play_pit(number)
    return half_game


@fixture
def finished_game():
    finished_game = KalahaGame(number_of_pits=6, starting_balls=6)
    while finished_game.get_current_player() is not None:
        try_pit = random.randint(0, 13)
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



def test_get_regular_pits():
    assert False


def test_get_player_balls_remaining():
    assert False


def test_get_player_score():
    assert False


def test_switch_player():
    assert False


def test_get_current_player():
    assert False


def test_check_endgame():
    assert False


def test_get_opposite_pit():
    assert False


def test_print_scores():
    assert False


def test_distribute_balls_from_pit():
    assert False


def test_determine_turn_end():
    assert False


def test_play_pit():
    assert False
