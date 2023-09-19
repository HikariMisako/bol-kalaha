from pytest import fixture, raises
from src.ball_pit import BallPit
from src.kalaha_enums import PitType, Player
from src.kalaha_errors import NotPlayableError


@fixture
def small_pit_player_1():
    ball_pit = BallPit(associated_player=Player.PLAYER_1, pit_type=PitType.SMALL)
    ball_pit.add_ball(3)
    return ball_pit


@fixture
def large_pit_player_1():
    ball_pit = BallPit(associated_player=Player.PLAYER_1, pit_type=PitType.LARGE)
    ball_pit.add_ball(3)
    return ball_pit


@fixture
def small_pit_player_2():
    ball_pit = BallPit(associated_player=Player.PLAYER_2, pit_type=PitType.SMALL)
    ball_pit.add_ball(3)
    return ball_pit


@fixture
def large_pit_player_2():
    ball_pit = BallPit(associated_player=Player.PLAYER_1, pit_type=PitType.LARGE)
    ball_pit.add_ball(3)
    return ball_pit


def test_get_ball_count(small_pit_player_1):
    # given a small ball pit for player 1 with 3 balls
    # when a ball is added
    assert small_pit_player_1.get_ball_count() == 3
    small_pit_player_1.add_ball()
    # then, the ball count should be 4
    assert small_pit_player_1.get_ball_count() == 4


def test_add_multiple_balls(small_pit_player_1):
    # given a small ball pit for player 1 with 3 balls
    # when 5 balls are added
    assert small_pit_player_1.get_ball_count() == 3
    small_pit_player_1.add_ball(5)
    # then the ball cound should be 8
    assert small_pit_player_1.get_ball_count() == 8


def test_wrong_ball_values(small_pit_player_1):
    # given a small ball pit for player 1
    # when zero or negative balls are added
    # then ValueErrors should be raised
    with raises(ValueError):
        small_pit_player_1.add_ball(0)
    with raises(ValueError):
        small_pit_player_1.add_ball(-1)


def test_empty_pit(small_pit_player_1):
    # given a small pit with 3 balls
    # when pit is emptied
    ball_count = small_pit_player_1.empty_pit()
    # then 3 balls should be returned
    # and the pit should be empty
    assert ball_count == 3
    assert small_pit_player_1.get_ball_count() == 0


def test_cannot_empty_large_pit(large_pit_player_1):
    # given any large pit with 3 balls
    # when trying to empty the large pit
    with raises(ValueError):
        large_pit_player_1.empty_pit()
    # then nothing should have changed and the pit should still have 3 balls
    assert large_pit_player_1.get_ball_count() == 3


def test_small_pit_is_playable(small_pit_player_1, small_pit_player_2):
    # given small pits for player 1 and player 2
    assert small_pit_player_1.is_playable(Player.PLAYER_1)
    assert small_pit_player_2.is_playable(Player.PLAYER_2)
    # when the wrong player is passed
    with raises(NotPlayableError):
        small_pit_player_1.is_playable(Player.PLAYER_2)
    with raises(NotPlayableError):
        small_pit_player_2.is_playable(Player.PLAYER_1)
    # then, NotPlayableError should be raised


def test_empty_small_pit_is_playable(small_pit_player_1, small_pit_player_2):
    # given empty small pits for player 1 and 2
    small_pit_player_1.empty_pit()
    small_pit_player_2.empty_pit()
    # when these are tried to be played by the right players
    with raises(NotPlayableError):
        small_pit_player_1.is_playable(Player.PLAYER_1)
    with raises(NotPlayableError):
        small_pit_player_2.is_playable(Player.PLAYER_2)
    # then, NotPlayableError should be raised


def test_large_pit_is_playable(large_pit_player_1, large_pit_player_2):
    # given any large pits with 3 balls
    # when these are tried to be played
    with raises(NotPlayableError):
        large_pit_player_1.is_playable(Player.PLAYER_1)
    with raises(NotPlayableError):
        large_pit_player_2.is_playable(Player.PLAYER_2)
    # NotPlayableError should be raised
    # and, there should still be 3 balls in the pits!
    assert large_pit_player_1.get_ball_count() == 3
    assert large_pit_player_2.get_ball_count() == 3
