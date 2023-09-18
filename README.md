# Kalaha

## Installation

Run the following commands:

`pip install poetry`

`poetry install`

## Running

# TODO

In order to launch the 'app' run the following in terminal:

`uvicorn main:app`

Note: add `--reload` during development for quicker edits

Then, open your favorite browser, and navigate to `http://127.0.0.1:8000/docs`  in order to try the API.

/new_game starts a new game with custom settings, default is 6 balls, pits and the 'normal' gamemode, where you only get
another turn if you end on your own large pit or on your own small pit that was empty.

/play_pit tries to play the pit at the given index from 0 to number_of_pits * 2 + 2

/get_scores gets the current status of the game in a readable format