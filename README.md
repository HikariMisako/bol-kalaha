# Kalaha

## Installation

Run the following commands:
Following requirements, install poetry  #todo install page of poetry

`poetry install`

If you face issues when using poetry install, any python 3.9 or above environment with `fastapi` 0.103.0 or above should
be able to run this project.

## Running the code

In order to launch the 'app' run the following in terminal:

`uvicorn bol_kalaha.main:app`

Note: add `--reload` during development for quicker edits

Then, open your favorite browser, and navigate to `http://127.0.0.1:8000/docs`  in order to try the API.

/new_game starts a new game with custom settings, default is 6 balls, pits and the 'normal' gamemode, where you only get
another turn if you end on your own large pit or on your own small pit that was empty.

/play_pit tries to play the pit at the given index from 0 to number_of_pits * 2 + 2

/get_scores gets the current status of the game in a readable format