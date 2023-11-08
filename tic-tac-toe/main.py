"""
TIC-TAC-TOE

Implementation of the game tic-tac-toe

- The players can choose their own marks (instead of just X and O)
- Rematches allowed
- It indexes the board from 1 to 9 (left to right, top to bottom)
"""

import random
from typing import Iterable

## character used to represent an empty space in the board
EMPTY_SPACE = '-'
## string used as divisor in the UI
DIV = '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'


def print_board(board: list) -> None:
    """
    - board - list with 10 spots representing the board (the first one is not used)
    """

    # row by row
    for i in range(1, 8, 3):
        print( f'{board[i]}\t{board[i+1]}\t{board[i+2]}' )
        print()


def read_number(command: str) -> int:
    """
    Reads a number between 1-9 from the user and returns it

    - command - string to be passed as argumeto to input()
    """

    while True:
        num = input(command)
        if not num.isdigit():
            print('Must be a number')
        else:
            num = int(num)
            if num not in range(1, 10):
                print('Must be between 1 and 9')
            else:
                return num


def read_position(board: list) -> int:
    """
    - board - list with 10 spots representing the board (the first one is not used)
    """

    while True:
        position = read_number('Where will you place your mark (1-9)? ')
        ## available position
        if board[position] == EMPTY_SPACE:
            break
        else:
            print('Space occupied')
    return position


def verify_win(board: list, mark: str) -> bool:
    """
    - board - list with 10 spots representing the board (the first one is not used)
    """

    # primary diagonal
    if board[1] == board[5] == board[9] == mark:
        return True
    # secondary diagonal
    elif board[3] == board[5] == board[7] == mark:
        return True
    else:
        # columns
        for i in range(1, 4):
            if board[i] == board[i+3] == board[i+6] == mark:
                return True
        # rows
        for i in range(1, 8, 3):
            if board[i] == board[i+1] == board[i+2] == mark:
                return True
        return False


def verify_tie(board: list) -> bool:
    """
    - board - list with 10 spots representing the board (the first one is not used)
    """

    return EMPTY_SPACE not in board


def play_game(players: Iterable[dict[str]]) -> None:
    """
    - players - iterable collection containing the players, which are
                 a dictionary containing their name and mark
    """

    random.shuffle(players) ## randomized play order
    board = [None] + [EMPTY_SPACE]*9 ## board[0] not used

    done = False
    while not done:
        for player in players:
            print_board(board)
            print(f"<< {player['name']} >>")
            position = read_position(board)
            board[position] = player['mark']

            print()
            print(DIV)
            print()

            if verify_win(board, player['mark']):
                print_board(board)
                print( f"Winner: {player['name']}" )
                print('Congratulations!!!')
                done = True
                break
            elif verify_tie(board):
                print_board(board)
                print('There was a tie')
                done = True
                break


print(r'  _   _        _               _             ')
print(r' | | (_)      | |             | |            ')
print(r' | |_ _  ___  | |_ __ _  ___  | |_ ___   ___ ')
print(r' | __| |/ __| | __/ _` |/ __| | __/ _ \ / _ \ ')
print(r' | |_| | (__  | || (_| | (__  | || (_) |  __/')
print(r'  \__|_|\___|  \__\__,_|\___|  \__\___/ \___|')
print()
print('Board layout:')
print()
print_board( [None] + list(range(1, 10)) )

players = []

# reading playerS id
for i in range(1, 3):
    print(f'<< Player {i} >>')
    name = input('Name: ')
    while True:
        mark = input('Mark: ')
        if len(mark) > 1:
            print('Please enter just one character')
        elif mark in (EMPTY_SPACE, '_'): ## '_' too similar to EMPTY_SPACE
            print('Invalid mark')
        else:
            break
    players.append( {'name': name, 'mark': mark} )
    print()

print(DIV)
print()

continue_playing = True
while continue_playing:
    play_game(players)
    print()

    while True:
        option = input('Continue playing (y/n)? ')
        if option in ('y', 'n'):
            break
        else:
            print('Invalid option!')
    if option == 'n':
        continue_playing = False
    else:
        print()
        print(DIV)
        print()
