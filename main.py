import os
from time import sleep
import connect4
import tris
from colorama import Fore, Style

games = {1:[tris.engine,'Tris (tic, tac, toe)',{
            1:[tris.random,'Mrs. RNG',0]}
            ],
        2:[connect4.engine,'Connect4',{
            1:[connect4.random,'Mrs. RNG',0],
            2:[connect4.extra_basic,'Mr. meh','???'],
            3:[connect4.basic,'Mr. Borges','???'],
            4:[connect4.medium,'Mrs. Plus','???']}
           ]
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

def _choose_game():
    while True:
        _clean_terminal()
        print()
        print('Welcome\n')

        for game in games:
            description = games[game][1]
            print(f'     {game} - {description}')
        
        try:
            choose = int(input(f'\nchoose one game to play: '))
        except ValueError:
            print('Insert a valid number! ')
            input("Press ENTER to retry...")
            continue
            
        if choose not in games:
            print('Insert a valid number! ')
            input("Press ENTER to retry...")
            continue
        break
    engine = games[choose][0]
    bot_list = games[choose][2]
    return engine, bot_list

def _Human(game):
    player = player_dict[game.current_player]

    choose = input(f'\n{player} choose one column: ')
    return choose

def _choose_bot(bot_list):
    while True:
        _clean_terminal()
        print('choose your opponent\n')
        print('0 - Human')
        for i in bot_list:
            name = bot_list[i][1]
            print(f'{i} - {name}')
        try:
            choose = int(input(f'choose one game to play: '))
        except ValueError:
            print('Insert a valid number! ')
            input("Press ENTER to retry...")
            continue
        
        if choose == 0:
            opponent = _Human
            break

        if choose not in bot_list:
            print('Insert a valid number! ')
            input("Press ENTER to retry...")
            continue
        opponent = bot_list[choose][0]
        break

    return(opponent)


def play():
    engine, bot_list = _choose_game()
    game = engine()
    player1 = _Human
    player2 = _choose_bot(bot_list)
    _clean_terminal()
    recursion = False
    while True:
        if game.move_number != 0 and not recursion:
            print(f'opponent played {choose}\n')
        recursion = False
        game.show_table()
        current_player = game.current_player
        if current_player == 1:
            if player2 != _Human:
                print(f'\n{player_dict[game.current_player]} are choosing, please wait',end='')
                for t in range(3):
                    sleep(0.5)
                    print('.',end='')
            choose = player2(game)
            r = game.play(choose)
            if not r:
                recursion = True
                print('Insert a valid move! ')
                input("Press ENTER to retry...")
                _clean_terminal()
                continue
        else:
            choose = player1(game)
            r = game.play(choose)
            if not r:
                recursion = True
                print('Insert a valid move! ')
                input("Press ENTER to retry...")
                _clean_terminal()
                continue
        
        end, winner = game.check_end()

        if end:
            break
        _clean_terminal()

    _clean_terminal()
    game.show_table()
    print()
    
    if winner == 0:
        print("it's a draw!")
    else:
        print(f'{player_dict[winner]} win!')

if __name__ == '__main__':
    play()




    
