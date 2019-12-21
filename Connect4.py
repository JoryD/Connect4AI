import sys
from random import randint, shuffle
from copy import deepcopy

CIRCLE_INVALID = -1
CIRCLE_EMPTY = 0
CIRCLE_YELLOW = 1
CIRCLE_RED = 2
CIRCLE_DRAW = 3
NO_WINNER = 4
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
AI_STRENGTH = 2000
emptyBoard = [[0 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]
cellOptions = [" ", "Y", "R"];


COLORAMA = False
CLEARABLE = False
RUSH = True
BX = BOARD_WIDTH - 1
BY = BOARD_HEIGHT - 1
BANNER = '''    _/_/_/                                                      _/      _/  _/   
  _/          _/_/    _/_/_/    _/_/_/      _/_/      _/_/_/  _/_/_/_/  _/  _/    
 _/        _/    _/  _/    _/  _/    _/  _/_/_/_/  _/          _/      _/_/_/_/   
_/        _/    _/  _/    _/  _/    _/  _/        _/          _/          _/      
 _/_/_/    _/_/    _/    _/  _/    _/    _/_/_/    _/_/_/      _/_/      _/    '''

SMALL_BANNER = ''' _                      
/  _ ._ ._  _  __|_|_|_ 
\_(_)| || |(/_(_ |_  |  '''

def Get(b, level, col):
    if (col < 0 or col > BX or level < 0 or level > BY):
        return CIRCLE_INVALID
    return b[level][col]

def Set(b, level, col, value):
    if col < 0 or col > BX or level < 0 or level > BY:
        return CIRCLE_INVALID
    b[level][col] = value

def ColIsFull(b, col):
    return (Get(b, BY, col) != CIRCLE_EMPTY)

def Drop(b, col, value):
    if (ColIsFull(b,col) == CIRCLE_INVALID):
        return 0
    for level in range(0,BOARD_HEIGHT):
        if Get(b,level,col) == CIRCLE_EMPTY:
            Set(b,level,col,value)
            break
    return 1

def printGameBoard(b):
    if CLEARABLE:
        os.system('cls||echo -e \\\\033c')
    if COLORAMA:
        print(colorama.Fore.YELLOW+SMALL_BANNER+colorama.Style.RESET_ALL)
    for level in range(BY,-1,-1):
        print(level, end='')
        for col in range(0, BOARD_WIDTH):
            color = Get(b,level,col)
            if COLORAMA:
                if color == CIRCLE_YELLOW:
                    print(colorama.Fore.YELLOW+"[Y]"+colorama.Style.RESET_ALL,end="")
                elif color == CIRCLE_RED:
                    print(colorama.Fore.RED+"[R]"+colorama.Style.RESET_ALL,end="")
                else:
                    print("[ ]",end="")
            else:
                print("[" + str(cellOptions[color]) + "]",end="")
        print()
    print(" ", end = "")
    for col in range(0, BOARD_WIDTH):
        print(" " + str(col) + " ", end="")
    print()

def GetWinner(b):
    empty = 0
    sp = 0
    for level in range(BY,0,-1):
        for col in range(0, BX-1):
            color = Get(b,level, col)
            if (color == CIRCLE_EMPTY):
                empty = empty + 1
                continue
            directory = [[1,0],[0,1],[1,1],[-1,1]]
            
            for d in range(0,4):
                start_col = col
                start_level = level
                while(Get(b,start_level-directory[d][1], start_col-directory[d][0]) == color):
                    start_col = start_col - directory[d][0]
                    start_level = start_level - directory[d][1]
                        
                count = 0
                while(Get(b,start_level,start_col) == color):
                    count = count + 1
                    start_col = start_col + directory[d][0]
                    start_level = start_level + directory[d][1]
                if (count >= 4):
                    return color
    if(empty <= BOARD_HEIGHT*BOARD_WIDTH):
        return CIRCLE_EMPTY
    return CIRCLE_DRAW

def RandomGame(b,tomove):
    for i in range(0,42):
        potentialMoves = [x for x in range(0,BOARD_WIDTH)]
        shuffle(potentialMoves)
        for move in potentialMoves:
            if(not ColIsFull(b,move)):
                nextMove = move
                break
        if (Drop(b,nextMove,tomove)):
            if(tomove == CIRCLE_YELLOW):
                tomove = CIRCLE_RED
            else:
                tomove = CIRCLE_YELLOW
        winner = GetWinner(b)
        if (winner != CIRCLE_EMPTY):
            return winner
    return CIRCLE_DRAW

def SuggestMove(b,tomove):
    best = -1
    best_ratio = 0
    if COLORAMA:
        if tomove == CIRCLE_YELLOW:
            print(colorama.Fore.YELLOW+"YELLOW IS THINKING"+colorama.Style.RESET_ALL)
        elif tomove == CIRCLE_RED:
            print(colorama.Fore.RED+"RED IS THINKING"+colorama.Style.RESET_ALL)
    for move in range(0,BX+1):
        if (ColIsFull(b,move)):
            continue # No valid move.
        won = 0
        lost = 0
        for j in range(0, AI_STRENGTH):
            copy = deepcopy(b)
            Drop(copy,move,tomove);
            if (GetWinner(copy) == tomove):
                return move
            if (tomove == CIRCLE_YELLOW):
                nextPlayer = CIRCLE_RED
            else:
                nextPlayer = CIRCLE_YELLOW
            winner = RandomGame(copy, nextPlayer)
            if (winner == CIRCLE_YELLOW or winner == CIRCLE_RED):
                if (winner == tomove):
                    won = won + 1
                else:
                    lost = lost + 1
            if j == AI_STRENGTH/2 and RUSH == True:
                ratio = float(won)/(lost+won+1);
                if(ratio <= best_ratio and best != -1):
                    if COLORAMA:
                        print(colorama.Fore.MAGENTA+"X"+colorama.Style.RESET_ALL, end = " ")
                    break
        ratio = float(won)/(lost+won+1);
        if(ratio > best_ratio or best == -1):
            best = move
            best_ratio = ratio
            if COLORAMA:
                print(colorama.Fore.GREEN+"$"+colorama.Style.RESET_ALL, end = " ")
        print("Move",move,":",(ratio*100));

    return best

def sim():
    board = emptyBoard[:]
    while(1):
        printGameBoard(board)
        if showPotentialWinner(board):  return
        Drop(board,SuggestMove(board,CIRCLE_RED),CIRCLE_RED)
        computer_move = SuggestMove(board,CIRCLE_YELLOW)
        Drop(board,computer_move,CIRCLE_YELLOW)
def singlePlayer():
    board = emptyBoard[:]
    while(1):
        printGameBoard(board)
        print(board)
        if showPotentialWinner(board):  return
        Drop(board,getMoveFromPlayer(board),CIRCLE_RED)
        computer_move = SuggestMove(board,CIRCLE_YELLOW)
        Drop(board,computer_move,CIRCLE_YELLOW)

def showPotentialWinner(board):
    if (GetWinner(board) != CIRCLE_EMPTY):
        if COLORAMA:
            print(colorama.Back.WHITE+colorama.Fore.BLACK+" winner: ",GetWinner(board), colorama.Style.RESET_ALL)
        else:
            print("winner: ",GetWinner(board))
        return True
    return False
            
def getMoveFromPlayer(b):
    human_move = -1
    while(human_move == -1):
        try:
            human_move = int(input("Red, state your move: "))
        except:
            print("Invalid move, try again!")
            human_move = -1
            continue           
        if (human_move > (BX) or human_move < 0):
            print("Invalid move, try again!")
            human_move = -1
        if (human_move != -1 and ColIsFull(b,human_move) != CIRCLE_EMPTY):
            print("Invalid move, try again!")
            human_move = -1
    return human_move    
def twoPlayer():
    board = emptyBoard[:]
    while(1):
        printGameBoard(board)
        if showPotentialWinner(board):  return          
        Drop(board,getMoveFromPlayer(board),CIRCLE_RED)
        human_move = -1
        Drop(board,getMoveFromPlayer(board),CIRCLE_YELLOW)

if __name__== "__main__":
    print(BANNER)
    print("By Jory Detwiler v1.0.0.0 | https://github.com/JoryD")
    if "--norush" in sys.argv:
        RUSH = False
    if "--pretty" in sys.argv:
        try:
            import colorama
            colorama.init()
            COLORAMA = 1
        except ImportError:
            print("You do not have COLORAMA installed. No colors for you :(")
            print("Try `pip install colorama`, `python pip install colorama`, `python3 pip install colorama`, or maybe `pip3 install colorama`")
    if "--clearable" in sys.argv:
        import os
        CLEARABLE = 1
    if "--singleplayer" in sys.argv:
        singlePlayer()
    elif "--multiplayer" in sys.argv:
        twoPlayer()
    else:
        sim()

