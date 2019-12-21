# Connect4AI
A monte carlo AI for Connect4 written in Python. This project was tested in Python 3.8 and should work with any Python 3 install.

# Usage:
  ```python Connect4.py``` runs simulated game
  
# Options:
 ``` --singleplayer ``` lets you play against the AI.
 
 ``` --multiplayer ``` lets you play against a friend (or yourself if you dont have any :().

  ``` --norush ``` will let the AI take its time, hey we aren't in a rush here!
  
  ``` --pretty ``` will allow you yo live in the world of color TV.
  
  ``` --clearable  ``` makes the console clear itself when the board redraws.

# Things to Tweak
```BOARD_WIDTH```, ```BOARD_HEIGHT```, and ```AI_STRENGTH``` can all be easily changed, just put in any non-zero positve integer.

``` BOARD_WIDTH ``` is the width of the game board.

``` BOARD_HEIGHT ``` is the height of the game board.

``` AI_STRENGTH ``` is how many simulations the AI runs on each of the possible moves.
  
# Inspiration
Inspired by https://github.com/antirez/connect4-montecarlo. Antirez did a great job writing his version in C. C is nice, however Python is the language of the gods.
