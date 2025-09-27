from random import choice
import os
from colorama import Fore, Style

class tris:
    def __init__(self):
        p1 = 1
        p2 = -1
        empty = 0
        self.grid_len = 3
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
        
        for i in range(-1,-(self.grid_len)-1,-1):
            row = self.board[i]
            print(f'{i+self.grid_len+1} ',end='')
            for j in range(self.grid_len):
                value = row[j]
                value = player_mark[value]
                print(f' {value} ', end='')
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
                    print(f' {i+1}  ',end='')

    def play(self,move):
        if not move in self.legit_move:
            return False
        row = move[0]
        col = move[1]

        self.board[row-1][col-1] = self.current_player
        self._switch_player()

if __name__ == "__main__":
    os.system('cls')
    game = tris()
    game.show_table()
    game.play((1,1))
    game.play((2,2))
    print('\n\n')
    game.show_table()