# Kalaha

## Installation

Install poetry according to the instructions:
https://python-poetry.org/docs/

Then, using some form of terminal inside the folder root folder (bol-kalaha) run the command:
`poetry install`

## Running the code

In order to launch the 'app' run the following in terminal inside the root folder (bol-kalaha):

`poetry run uvicorn src.main:app`

Note: add `--reload` during development for quicker edits

Then, open your favorite browser, and navigate to `http://127.0.0.1:8000/`  in order to try the API.

/new_game starts a new game with custom settings, default is 6 balls, pits and the 'normal' gamemode, where you only get
another turn if you end on your own large pit or on your own small pit that was empty.

/play_pit tries to play the pit at the given index from 0 to number_of_pits * 2 + 2

/get_scores gets the current status of the game in a readable format

/get_all_pits returns all the current pits in a list, useful in the future

## Running the unit tests
`poetry run python -m pytest tests/`