from fastapi.testclient import TestClient
from pytest import fixture
from src.kalaha_enums import GameType
from src.main import app, manager

game_outcome_text = "Game is ongoing!"
player_turn_text = "Current player: PLAYER_1"


@fixture
def client() -> TestClient:
    # set up a new game every time!
    manager.new_game(number_of_pits=6, starting_balls=6, game_type=GameType.BOL_DEFAULT)
    return TestClient(app)


def test_get_scores(client):
    # given a clean start
    # when scores are requested
    response = client.get("/get_scores")
    # then a 200 response code, a game outcome and player 1 should be returned
    assert response.status_code == 200
    assert "scores_list" in response.json().keys()
    assert response.json().get("game_outcome") == game_outcome_text
    assert response.json().get("player_turn") == player_turn_text


def test_get_all_pits(client):
    # given any state
    # when all pits are requested
    response = client.get("/get_all_pits")
    # then a 200 response code and a pit list should _always_ be returned
    assert response.status_code == 200
    assert "pit_list" in response.json().keys()


# new_game
def test_new_game(client):
    # given any state
    # when a new game is started
    data = {"starting_balls": 6, "number_of_pits": 6, "game_type": GameType.BOL_DEFAULT}
    response = client.put("/new_game", json=data)
    # then, player 1 should have the turn and the game should be ongoing
    assert response.json().get("game_outcome") == game_outcome_text
    assert response.json().get("player_turn") == player_turn_text


def test_wikipedia_version(client):
    # given: wikipedia version of game started with fewer balls than pits
    data = {
        "starting_balls": 2,
        "number_of_pits": 6,
        "game_type": GameType.WIKIPEDIA_VERSION,
    }
    response = client.put("/new_game", json=data)
    assert response.json().get("player_turn") == player_turn_text
    # when: pit 1 is played
    play_data = {"selected_pit": 1}
    play_response = client.put("/play_pit", json=play_data)

    # then, player 1 should still have the turn, he ended on his own pit
    assert play_response.json().get("player_turn") == player_turn_text


def test_single_pit(client):
    # given: clean setup
    # when: pit #1 is played
    data = {"selected_pit": 1}
    response = client.put("/play_pit", json=data)

    # then: a proper response is given, game is ongoing and turn goes to player 2!
    assert response.json().get("game_outcome") == game_outcome_text
    # after playing pit # 1, with the default starting setup, player 2 should have the turn
    assert response.json().get("player_turn") != player_turn_text


def test_single_pit_error(client):
    # given: clean setup
    # when: pit #9 is played
    data = {"selected_pit": 9}
    response = client.put("/play_pit", json=data)
    print(response)

    # then: an error should have been raised!
    assert response.status_code == 400
