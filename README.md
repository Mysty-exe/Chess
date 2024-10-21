# Multiplayer CHESS
This is a basic version of Chess. The objective is to take out the opponents king.

The control keys are:
- "mouse"

Used libraries:
- pygame
- socket
- uuid
- threading
- random
- json
- math


## Setup

Pre-requirements:

* python 3.9 >

## Run the app

First, make sure that you're in the right directory. If you're not, run
```
cd .../Chess
```

Open a terminal and run
```
python server.py
```

Open another terminal and run

```shell
python main.py
```

If you have another computer, run the same line again on that computer on a terminal (Must be connected to the same wifi). If you don't have another computer, you can open a new terminal and run the line of code again. 

## Troublshooting

- If you are using two computers, try to turn off the firewall as it may mess up the connection

## Limitations

- Computer that isn't running the server may crash if too much data is being sent per second

## Screenshots

![Menu](Assets/Screenshots/menu.png)
![Lobby](Assets/Screenshots/lobby.png)
![Game](Assets/Screenshots/game.png)
![Check](Assets/Screenshots/check.png)
![Forfeit](Assets/Screenshots/forfeit.png)
![Checkmate](Assets/Screenshots/checkmate.png)

## Rules

Read up on the rules here: **[CHESS Rules](https://www.chesshouse.com/pages/chess-rules)**
