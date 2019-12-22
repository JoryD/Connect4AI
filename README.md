# Connect4AI
A [Monte Carlo](https://en.wikipedia.org/wiki/Monte_Carlo_method) AI for [Connect4](https://en.wikipedia.org/wiki/Connect_Four) written in [Python](https://python.org). 

This project was tested in Python 3.8 and should work with any Python 3 install.

# Usage:
  ```python Connect4.py``` will run a simulated game AI vs AI.
  
# Options:
 ``` --singleplayer ``` lets you play against the AI.
 
 ``` --multiplayer ``` lets you play against a friend (or yourself if you dont have any :().

  ``` --norush ``` will let the AI take its time, hey we aren't in a rush here!
  
  ``` --rush ``` will make the AI rush its simulations if simulations are not proving favorable. This is on by default. 
  
  ``` --pretty ``` will allow you to live in the world of color TV. Makes use of [Colorama](https://pypi.org/project/colorama/)
  
  ``` --clearable  ``` makes the console clear itself when the board redraws.
  ``` --first``` and ```--second``` lets you choose if you go first or not.
  
  ``` --easy ```,``` --medium ```,``` --hard ```,``` --insane ```,``` --master ```,``` --demigod ```, ```--god``` are difficulty options, see if you can beat them all! However after insane the computer takes forever to move depending on your CPU single threaded performance.

# Things to Tweak
```BOARD_WIDTH```, ```BOARD_HEIGHT```, and ```AI_STRENGTH``` can all be easily changed, just put in any non-zero positve integer.

``` BOARD_WIDTH ``` is the width of the game board.

``` BOARD_HEIGHT ``` is the height of the game board.

``` AI_STRENGTH ``` is how many simulations the AI runs on each of the possible moves.

# Potential Improvements
Multithreading/Multiprocessing - run all 7 possible move simulations in parallel. Might not make sense considering the GIL.
  
# Inspiration
Inspired by https://github.com/antirez/connect4-montecarlo. Antirez did a great job writing his version in C. C is nice, however Python is the language of the gods.
