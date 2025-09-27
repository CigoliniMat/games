from random import choice
import os
from colorama import Fore, Style

class tris:
    def __init__(self):
        self.grid_len = 3
        self.number_to_win = 3
        self.board = []
        self.legit_move = []
        self._init_board()
        self.current_player = choice([-1,1])
        self.char_dict = [0,'A','B','C']
        

    def _init_board(self):
        for i in range(self.grid_len):
            self.board.append([])
        for i in range(self.grid_len):
            for j in range(self.grid_len):
                self.board[i].append(0)
                self.legit_move.append((i+1,j+1))
    
    def _switch_player(self):
        self.current_player = self.current_player*-1

    def show_table(self):
        player_mark = {0:' ',
                       1:'X',
                       -1:'O'}
        
        ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        for i in range(-1,-(self.grid_len)-1,-1):
            row = self.board[i]
            print(Fore.LIGHTBLACK_EX,end='')
            value = ALPHABET[i+self.grid_len]
            print(f'{value} ',end='')
            print(Style.RESET_ALL,end='')
            for j in range(self.grid_len):
                value = row[j]
                value = player_mark[value]
                if row[j] == 1:
                    print(Fore.BLUE,end='')
                else:
                    print(Fore.RED,end='')
                print(f' {value} ', end='')
                print(Style.RESET_ALL,end='')
                if j < self.grid_len-1:
                    print('|',end='')
            print()
            if i > -self.grid_len:
                print('  ',end='')
                for n in range(self.grid_len):
                    print('---',end='')
                    if n < self.grid_len-1:
                        print('+',end='')
                    else:
                        print()
            else:
                print('  ',end='')
                for i in range(self.grid_len):
                    print(Fore.LIGHTBLACK_EX,end='')
                    print(f' {i+1}  ',end='')

    def play(self,move):
        if not move in self.legit_move:
            return False
        row = move[0]
        col = move[1]

        self.board[row-1][col-1] = self.current_player
        self._switch_player()

    def check_win(self):
        direction = [(0,1),(1,0),(1,1),(1,-1)]

        for x in range(0,self.grid_len):
            for y in range(0,self.grid_len):
                for off_x, off_y in direction:
                    count = 0
                    player = 0
                    for n in range(0, self.number_to_win):
                        x1 = x+(off_x * n)
                        y1 = y+(off_y * n)
                        print(f'x1={x1} - y1={y1}')

                        if not 0 >= x1 > self.grid_len:
                            break
                        if not 0 >= y1 > self.grid_len:
                            break
                        value = self.board[x1][y1]
                        if value == 0:
                            break
                        if player == 0:
                            player = value
                            count += 1
                        elif player == value:
                            count += 1
                        else:
                            break

                        if count >= self.number_to_win:
                            return True, player
        return(False,0)

if __name__ == "__main__":
    os.system('cls')
    game = tris()
    game.show_table()
    game.play((3,1))
    game.play((2,1))
    game.play((2,2))
    game.play((2,3))
    game.play((1,3))
    print('\n\n')
    game.show_table()
    print('\n\n')
    print(game.check_win())