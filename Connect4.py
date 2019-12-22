import sys
from random import randint, shuffle
from copy import deepcopy

BOARD_WIDTH = 7
BOARD_HEIGHT = 6
AI_STRENGTH = 500
cellOptions = [" ", "Y", "R"]; # empty, Yellow symbol, Red symbol

CIRCLE_INVALID = -1
CIRCLE_EMPTY = 0
CIRCLE_YELLOW = 1
CIRCLE_RED = 2
CIRCLE_DRAW = 3
NO_WINNER = 4
COLORAMA = False
CLEARABLE = False
RUSH = True
emptyBoard = [[0 for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGHT)]
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
    if col < 0 or col > BX or level < 0 or level > BY:
        return CIRCLE_INVALID
    return b[level][col]


def Set(b, level, col, value):
    b[level][col] = value


def ColIsFull(b, col):
    return (Get(b, BY, col) != CIRCLE_EMPTY)


def Drop(b, col, value):
    if (ColIsFull(b,col) == CIRCLE_INVALID):
        return 0
    for level in range(0,BOARD_HEIGHT):
        if Get(b, level, col) == CIRCLE_EMPTY:
            Set(b, level, col, value)
            break
    return 1
    
    
def printGameBoard(b):
    if CLEARABLE:
        os.system('cls||echo -e \\\\033c')
    if COLORAMA:
        print(colorama.Fore.YELLOW + SMALL_BANNER + colorama.Style.RESET_ALL)
    else:
        print(SMALL_BANNER)
    for level in range(BY, -1, -1):
        print(level, end='')
        for col in range(0, BOARD_WIDTH):
            color = Get(b, level, col)
            if COLORAMA:
                if color == CIRCLE_YELLOW:
                    print(colorama.Fore.YELLOW+"[Y]"+colorama.Style.RESET_ALL, end="")
                elif color == CIRCLE_RED:
                    print(colorama.Fore.RED+"[R]"+colorama.Style.RESET_ALL, end="")
                else:
                    print("[ ]", end="")
            else:
                print("[" + str(cellOptions[color]) + "]", end="")
        print()
    print(" ", end = "")
    for col in range(0, BOARD_WIDTH):
        print(" " + str(col) + " ", end="")
    print()


def GetWinner(b):
    empty = 0
    sp = 0
    for level in range(BY, -1, -1):
        for col in range(0, BX):
            color = Get(b, level, col)
            if (color == CIRCLE_EMPTY):
                empty = empty + 1
                continue
            directory = [[1,0],[0,1],[1,1],[-1,1]]
            
            for d in range(0, 4):
                start_col = col
                start_level = level
                while(Get(b, start_level-directory[d][1], start_col-directory[d][0]) == color):
                    start_col = start_col - directory[d][0]
                    start_level = start_level - directory[d][1]
                        
                count = 0
                while(Get(b, start_level, start_col) == color):
                    count = count + 1
                    start_col = start_col + directory[d][0]
                    start_level = start_level + directory[d][1]
                if (count >= 4):
                    return color
    if(empty <= BOARD_HEIGHT * BOARD_WIDTH):
        return CIRCLE_EMPTY
    return CIRCLE_DRAW


def RandomGame(b, tomove):
    for i in range(0,42):
        potentialMoves = [x for x in range(0,BOARD_WIDTH)]
        shuffle(potentialMoves)
        for move in potentialMoves:
            if(not ColIsFull(b, move)):
                nextMove = move
                break
        if (Drop(b, nextMove, tomove)):
            if(tomove == CIRCLE_YELLOW):
                tomove = CIRCLE_RED
            else:
                tomove = CIRCLE_YELLOW
        winner = GetWinner(b)
        if (winner != CIRCLE_EMPTY):
            return winner
    return CIRCLE_DRAW


def SuggestMove(b, tomove, simulations=AI_STRENGTH):
    best = -1
    best_ratio = 0
    if COLORAMA:
        if tomove == CIRCLE_YELLOW:
            print(colorama.Fore.YELLOW + "YELLOW IS THINKING" + colorama.Style.RESET_ALL)
        elif tomove == CIRCLE_RED:
            print(colorama.Fore.RED + "RED IS THINKING" + colorama.Style.RESET_ALL)
    for move in range(0,BX+1):
        if (ColIsFull(b,move)):
            continue
        won = 0
        lost = 0
        draw = 0
        print_neutral = 1
        for j in range(0, simulations):
            copy = deepcopy(b)
            Drop(copy, move, tomove);
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
            else:
                draw = draw + 1
            if j == AI_STRENGTH/2 and RUSH == True:
                ratio = float(won)/(lost+won+1);
                if(ratio+0.05 <= best_ratio and best != -1):
                    if COLORAMA:
                        print(colorama.Fore.RED + "X" + colorama.Style.RESET_ALL, end = " ")
                        print_neutral = 0
                    break
        ratio = float(won)/(lost+won+1);
        if(ratio > best_ratio or best == -1):
            best = move
            best_ratio = ratio
            if COLORAMA:
                print(colorama.Fore.GREEN + "$" + colorama.Style.RESET_ALL, end = " ")
                print_neutral = 0
        if COLORAMA and print_neutral == 1:
            print(colorama.Fore.YELLOW + "?" + colorama.Style.RESET_ALL, end = " ")
        print("Move", move, ":", round(ratio*100,1), " draws: ", draw,);

    return best


def sim():
    board = deepcopy(emptyBoard)
    while(1):
        printGameBoard(board)
        if showPotentialWinner(board):  return
        Drop(board,SuggestMove(board, CIRCLE_RED, AI_STRENGTH), CIRCLE_RED)
        if showPotentialWinner(board):  return
        printGameBoard(board)
        Drop(board, SuggestMove(board, CIRCLE_YELLOW, AI_STRENGTH), CIRCLE_YELLOW)

        
def singlePlayer():
    board = deepcopy(emptyBoard)
    while(1):
        printGameBoard(board)
        if showPotentialWinner(board):  return
        Drop(board, getMoveFromPlayer(board), CIRCLE_RED)
        printGameBoard(board)
        print(board)
        if showPotentialWinner(board):  return
        computer_move = SuggestMove(board, CIRCLE_YELLOW, AI_STRENGTH)
        Drop(board, computer_move, CIRCLE_YELLOW)


def showPotentialWinner(board):
    winner = GetWinner(board)
    if winner != CIRCLE_EMPTY and winner != CIRCLE_DRAW:
        printGameBoard(board)
        if COLORAMA:
            if winner == CIRCLE_YELLOW:                
                print(colorama.Fore.YELLOW+" winner: YELLOW" + colorama.Style.RESET_ALL)
            else:
                print(colorama.Fore.RED+" winner: RED" + colorama.Style.RESET_ALL)
            return True    
        else:
            print("winner: ", winner)
            return True
    elif winner == CIRCLE_DRAW:
        printGameBoard(board)
        print("DRAW!")
    return False
            
def getMoveFromPlayer(b, color):
    potentialPlayerMove = -1
    while(potentialPlayerMove == -1):
        try:
            potentialPlayerMove = int(input("Player "+ str(color) +", state your move: "))
        except ValueError:
            print("Invalid move, try again!")
            potentialPlayerMove = -1
            continue
        if potentialPlayerMove == 9:
            return SuggestMove(b, color)
        if (potentialPlayerMove > (BX) or potentialPlayerMove < 0):
            print("Invalid move, try again!")
            potentialPlayerMove = -1
        if (potentialPlayerMove != -1 and ColIsFull(b, potentialPlayerMove) != CIRCLE_EMPTY):
            print("Invalid move, try again!")
            potentialPlayerMove = -1
    return potentialPlayerMove


def twoPlayer():
    board = deepcopy(emptyBoard)
    while(1):
        printGameBoard(board)
        if showPotentialWinner(board):  return          
        Drop(board, getMoveFromPlayer(board, CIRCLE_RED), CIRCLE_RED)
        printGameBoard(board)
        potentialPlayerMove = -1
        if showPotentialWinner(board):  return
        Drop(board, getMoveFromPlayer(board, CIRCLE_YELLOW), CIRCLE_YELLOW)
        

if __name__== "__main__":
    print(BANNER)
    print("By Jory Detwiler v1.0.0.0 | https://github.com/JoryD")
    if "--easy" in sys.argv:
        AI_STRENGTH = 250
    elif "--medium" in sys.argv or "--med" in sys.argv:
        AI_STRENGTH = 500
    elif "--hard" in sys.argv:
        AI_STRENGTH = 1000
        
    elif "--insane" in sys.argv:
        AI_STRENGTH = 2500
        
    elif "--master" in sys.argv:
        AI_STRENGTH = 5000
        
    elif "--demigod" in sys.argv:
        AI_STRENGTH = 10000
        
    elif "--god" in sys.argv:
        AI_STRENGTH = 100000
        
    if "--norush" in sys.argv:
        RUSH = False
        
    elif "--rush" in sys.argv:
        RUSH = True
        
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
        
        
