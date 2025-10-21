# Breakout Game

This project is a simple implementation of the classic Breakout game using Python. The game involves a paddle that the player controls to bounce a ball and break bricks arranged at the top of the screen.

## Project Structure

```
breakout-python
├── src
│   └── game.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Files Description

- **src/game.py**: Contains the main logic of the Breakout game, including the initialization, main loop, user input handling, collision detection, and game state updates. The main classes are:
  - `Game`: Manages the game's initialization and execution with methods like `run`, `update`, and `draw`.
  - `Ball`: Manages the ball's position and speed with methods like `move` and `bounce`.
  - `Paddle`: Manages the paddle's position with the `move` method.
  - `Brick`: Manages the state of the bricks with the `hit` method.

- **requirements.txt**: Lists the external libraries required for the project, such as `pygame`.

- **.gitignore**: Defines files and directories to be ignored by Git, such as `__pycache__/`.

## Installation

To run the game, you need to have Python installed on your machine. You can install the required libraries using pip:

```
pip install -r requirements.txt
```

## Usage

After installing the required libraries, you can run the game by executing the following command:

```
python src/game.py
```

Enjoy playing the Breakout game!