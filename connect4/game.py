import os
from engine import connect4
from time import sleep
import algorithm.hard_coded as hd
from algorithm.random import random

pc_dict = {
    1:{'f':random,'name':'random','difficulty':0},
    2:{'f':hd.extra_basic,'name':'easy algorithm','difficulty':'???'},
    3:{'f':hd.basic,'name':'algorithm', 'difficulty':'???'},
    4:{'f':hd.medium,'name':'medium algorithm', 'difficulty':'???'},
    }

player_dict = {0:'blank',#' '
                   -1:'player1',#X
                   1:'player2'#O
                   }

def _clean_terminal():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

def _choose_mode(player):
    while True:
        max_item = 0
        _clean_terminal()
        for item in pc_dict:
            algoritmh = pc_dict[item]
            print(f'{item} - {algoritmh['name']}, difficulty={algoritmh['difficulty']}')
            max_item = item
        options = list(range(1,max_item+1))
        try:
            choose = int(input(f'\nchoose a algorithm to challenge (from 1 to {max_item}): '))
        except ValueError:
            print('Insert a valid number! ')
            input("Press ENTER to retry...")
            continue
        if choose in options:
            player_dict[player] = pc_dict[choose]['name']
            return pc_dict[choose]['f']
        else:
            print(f'choose a number from 1 to {max_item} ')
            input("Press ENTER to retry...")
    
def Human(game):
    player = player_dict[game.current_player]

    while True:
        try:
            choose = int(input(f'\n{player} choose one column: '))
        except ValueError:
            print('Insert a valid number! ')
            input("Press ENTER to retry...")
            _clean_terminal()
            game.show_table()
            continue

        if choose not in game.legit_move:
            print('Insert a valid column! ')
            input("Press ENTER to retry...")
            _clean_terminal()
            game.show_table()
            continue
        return choose

def p1_vs_p2(player1=0,player2=0,start_player=0,testing=False):
    if not testing:
        _clean_terminal()
    if player1 == Human:
        while True:
            try:
                name = str(input(f'Player1 choose a name: '))
                name = name.lstrip()
                if len(name)>0:
                    player_dict[-1] = name
                else:
                    continue
                break
            except ValueError:
                print('Insert a valid name! ')
                continue
    elif player1 == 0:
        player1 = _choose_mode(-1)
    if player2 == Human:
        while True:
            try:
                name = str(input(f'Player2 choose a name: '))
                name = name.lstrip()
                if len(name)>0:
                    player_dict[1] = name
                else:
                    continue
                break
            except ValueError:
                print('Insert a valid name! ')
                continue
    elif player2 == 0:
        player2 = _choose_mode(1)

    game = connect4()
    if start_player != 0:
        game.current_player = start_player
    if not testing:
        _clean_terminal()
        print(f'Welcome to connect{game.win_number},')
        print(f'choose a column to fill the button row, the first that connect{game.win_number} pawn Win!')
        print(f'\nthe {player_dict[game.current_player]} start!\n')
    
    end = False
    while end == False:
        if game.move_number > 0:
            if not testing:
                print(f'{player_dict[game.current_player*-1]} choose column n.{choose}\n')
        if not testing:
            game.show_table()
        if game.current_player == -1:
            if player1 != Human:
                if not testing:
                    print(f'\n{player_dict[game.current_player]} are choosing, please wait',end='')
                    for t in range(3):
                        sleep(0.5)
                        print('.',end='')
            choose = player1(game)
        else:
            if player2 != Human:
                if not testing:
                    print(f'\n{player_dict[game.current_player]} are choosing, please wait',end='')
                    for t in range(3):
                        sleep(0.5)
                        print('.',end='')
            choose = player2(game)

        game.play(choose)
        end, winner = game.check_end()
        game.switch_player()
        if not testing:
            _clean_terminal()
    
    if winner == 0:
        if not testing:
            game.show_table()
            print(f"\nIt's a draw!")
    else:
        if not testing:
            game.show_table()
            print(f'\n{player_dict[winner]} won!\n')
    
    return(winner)

if __name__ == '__main__':
    
    if True:
        p1_vs_p2(Human)
    else:
        score = {-1:0,0:0,1:0}
        players = [-1,1]
        for i in range(1000):
            start = players[i%2]
            result = p1_vs_p2(hd.medium,random,testing=True, start_player=start)
            score[result] += 1

        print(score)    
