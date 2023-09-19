from src.ball_pit import BallPit
from pytest import fixture, raises


@fixture
def small_pit_player_a():
    ball_pit = BallPit(True, "small")
    ball_pit.add_ball(3)
    return ball_pit


@fixture
def large_pit_player_a():
    ball_pit = BallPit(True, "large")
    ball_pit.add_ball(3)
    return ball_pit


@fixture
def small_pit_player_b():
    ball_pit = BallPit(False, "small")
    ball_pit.add_ball(3)
    return ball_pit


@fixture
def large_pit_player_b():
    ball_pit = BallPit(False, "large")
    ball_pit.add_ball(3)
    return ball_pit


def test_get_ball_count(small_pit_player_a):
    assert small_pit_player_a.get_ball_count() == 3
    small_pit_player_a.add_ball()
    assert small_pit_player_a.get_ball_count() == 4
    small_pit_player_a.empty_pit()
    assert small_pit_player_a.get_ball_count() == 0


def test_add_ball(small_pit_player_a):
    assert small_pit_player_a.get_ball_count() == 3
    small_pit_player_a.add_ball()
    assert small_pit_player_a.get_ball_count() == 4
    small_pit_player_a.add_ball(5)
    assert small_pit_player_a.get_ball_count() == 9
    with raises(ValueError):
        small_pit_player_a.add_ball(0)
    with raises(ValueError):
        small_pit_player_a.add_ball(-1)


def test_empty_pit(small_pit_player_a, large_pit_player_a):
    assert small_pit_player_a.empty_pit() == 3
    assert small_pit_player_a.empty_pit() == 0
    small_pit_player_a.add_ball()
    assert small_pit_player_a.empty_pit() == 1
    with raises(ValueError):
        large_pit_player_a.empty_pit()


def test_match_player(small_pit_player_a, small_pit_player_b):
    assert small_pit_player_a.match_player(True)
    assert small_pit_player_b.match_player(False)
    assert not small_pit_player_a.match_player(False)
    assert not small_pit_player_b.match_player(True)


def test_is_small(small_pit_player_a, small_pit_player_b):
    assert small_pit_player_a.is_small()
    assert not small_pit_player_a.is_large()
    assert small_pit_player_b.is_small()
    assert not small_pit_player_b.is_large()
    assert small_pit_player_a.is_small() != small_pit_player_a.is_large()
    assert small_pit_player_b.is_small() != small_pit_player_b.is_large()


def test_is_large(large_pit_player_a, large_pit_player_b):
    assert not large_pit_player_a.is_small()
    assert large_pit_player_a.is_large()
    assert not large_pit_player_b.is_small()
    assert large_pit_player_b.is_large()
    assert large_pit_player_a.is_small() != large_pit_player_a.is_large()
    assert large_pit_player_b.is_small() != large_pit_player_b.is_large()


def test_is_playable(
    small_pit_player_a, small_pit_player_b, large_pit_player_a, large_pit_player_b
):
    assert small_pit_player_a.is_playable(True)
    assert small_pit_player_b.is_playable(False)
    with raises(ValueError):
        small_pit_player_a.is_playable(False)
    with raises(ValueError):
        small_pit_player_b.is_playable(True)
    with raises(ValueError):
        large_pit_player_a.is_playable(True)
    with raises(ValueError):
        large_pit_player_b.is_playable(False)

    small_pit_player_a.empty_pit()
    small_pit_player_b.empty_pit()
    with raises(ValueError):
        small_pit_player_a.is_playable(True)
    with raises(ValueError):
        small_pit_player_b.is_playable(True)
