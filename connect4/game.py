import os
from engine import connect4

def _clean_terminal():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

def human_vs_human():
    player_dict = {0:'blank',#' '
                   -1:'Cross',#X
                   1:'Circle'#O
                   }
    
    game = connect4()
    _clean_terminal()
    print(f'Welcome to connect{game.win_number},')
    print(f'choose a column to fill the button row, the first that connect{game.win_number} pawn Win!')
    print(f'\nthe {player_dict[game.current_player]} start!\n')
    
    end = False
    while end == False:
        game.show_table()
        try:
            print(f'\nmove number {game.move_number}')
            choose = int(input(f'{player_dict[game.current_player]} choose one column: '))
        except ValueError:
            print('Insert a valid number! ')
            input("Press ENTER to retry...")
            _clean_terminal()
            continue

        if choose not in game.legit_move:
            print('Insert a valid column! ')
            input("Press ENTER to retry...")
            _clean_terminal()
            continue

        game.insert_pawn(choose)
        end, winner = game.check_end()
        _clean_terminal()
    
    game.show_table()
    if winner == 0:
        print(f"\nIt's a draw!")
    else:
        print(f'\n{player_dict[game.current_player]} won!\n')

if __name__ == '__main__':
    human_vs_human()    