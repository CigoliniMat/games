import os
from random import choice

column_number = 7
row_number = 6
number_to_win = 4

column_range = list(range(1,column_number+1))
row_range = list(range(1,row_number+1))
valide_move = list(range(1,column_number+1))

dictionary = {None:'blank',
              0:'p1',
              1:'p2'}
mark_dict = {None:' ',
              0:'X',
              1:'O'}

board = []

for row in row_range:
    board.append([])
    for column in column_range:
        board[row-1].append(None)

def show_board():
    if os.name == 'nt':
        os.system('cls')
        pass
    else:
        os.system('clear')

    print('\n'*3)
    for row in reversed(board):
        print(' '*3,end='')
        for value in row:
            mark = mark_dict[value]
            print(f'| {mark} ', end='')
        print('|')
        print(' '*3,end='')
        for value in row:
            print('+---',end='')
        print('+')

    print(' '*3,end='')
    for n in column_range:
        print(f'| {n} ', end='')
    print('|')

def play(column, player):
    for row in row_range:

        if board[row-1][column-1] == None:
            board[row-1][column-1] = player
            if row == row_number:
                valide_move.remove(column)
            return

def verify_win():
    def verify_sequence(sequence, n_for_win=number_to_win):
        count = 0
        prev_value = None
        for value in sequence:
            if value == prev_value:
                count += 1
            else:
                prev_value = value
                count = 1
            if count >= n_for_win and value != None:
                return True, value
        return False, None
    
    #verify row point
    for row in board:
        success, player = verify_sequence(row)
        if success:
            return success,player
    
    #verify column point
    for column in column_range:
        vertical_sequence = []
        for row in board:
            vertical_sequence.append(row[column-1])
        success, player = verify_sequence(vertical_sequence)
        if success:
            return success,player
    
    #verify oblique point
    point_range = range(1,number_to_win)
    for row in row_range: #for each box in the table
        row -= 1
        for column in column_range:
            column -= 1
            dx_sequence = []
            sx_sequence = []
            dx_sequence.append(board[row][column])
            sx_sequence.append(board[row][column])

            for point in point_range:
                if row + point < row_number and column + point < column_number:
                    dx_sequence.append(board[row+point][column+point])
                if row + point < row_number and column - point > 0:
                    sx_sequence.append(board[row+point][column-point])

            if len(dx_sequence) >= number_to_win:
                success, player = verify_sequence(dx_sequence)
            if success:
                return success,player
            
            if len(sx_sequence) >= number_to_win:
                success, player = verify_sequence(sx_sequence)
            if success:
                return success,player

    return False,None

def game():
    show_board()
    move = 0
    random_start = choice([0,1]) #the choice start the game
    while True:
        if move%2 == random_start:
            player = 0
        else:
            player = 1

        try:
            choose = int(input(f'\n{player} choose a column:'))
        except:
            print('select a valid column')
            continue

        if not choose in valide_move:
            print('select a valid column')
            continue
        play(choose,player)
        show_board()
        success, player = verify_win()
        
        if success:
            print(f'{mark_dict[player]} Win!')
            break

        move += 1


if __name__ == '__main__':
    pass
    game()