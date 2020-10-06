from menu import *
import threading

# Testing

# Create menu
Menu()


"""
BUGS:
Final move needs to be handled with the clock
If gameover pause clock and stop updating it's display

Threat by pawns slightly dodgy when pieces captured
when pawn captures pawn

in engine decision logic it is printing checkmate to console when checkmates are impossible within the search depth

Engine did not stop mate in one

Engine stalemated instead of winning


DO depth 4 before doing depth 3 with alpha beta pruning


current moves and off them branches of possible boards 


Add idea of outposts to score function

IMPROVEMENTS:
Add a game over screen instead of returning out of the new game function
If clock runs out of time... game over is true and go to game over screen

Game over screen:
Option to save the game
Option to replay the game

"""
