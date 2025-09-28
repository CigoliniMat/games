from random import choice
import os
from colorama import Fore, Style
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class tris:
    bot = {}
    
    def __init__(self):
        self.grid_len = 3
        self.number_to_win = 3
        self.move_number = 0
        self.board = []
        self.legit_move = []
        self._init_board()
        self.current_player = choice([-1,1])
        
    def _init_board(self):
        for i in range(self.grid_len):
            self.board.append([])
        for i in range(self.grid_len):
            for j in range(self.grid_len):
                self.board[i].append(0)
                self.legit_move.append((i,j))
    
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
                    print(Style.RESET_ALL,end='')

    def play(self,move):
        if isinstance(move,str):
            #if the input came from a human
            #instead of 0 he start from 1 and use char for row ex. A1 = 0,0
            if len(move) != 2:
                return False
            row_char = move[0]
            try:
                col = int(move[1])-1
            except:
                return False
            row = ALPHABET.find(row_char) 
            move = (row,col)
        row = move[0]
        col = move[1]

        if not move in self.legit_move:
            return False

        self.board[row][col] = self.current_player
        self.legit_move.remove(move)
        self._switch_player()
        self.move_number += 1
        return True

    def check_end(self):
        if len(self.legit_move) == 0:
            return True,0
        direction = [(0,1),(1,0),(1,1),(1,-1)]

        for x in range(0,self.grid_len):
            for y in range(0,self.grid_len):
                for off_x, off_y in direction:
                    count = 0
                    player = 0
                    for n in range(0, self.number_to_win):
                        x1 = x+(off_x * n)
                        y1 = y+(off_y * n)

                        if not self.grid_len > x1 >= 0:
                            break
                        if not self.grid_len > y1 >= 0:
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
        return False,0

if __name__ == "__main__":
    os.system('cls')
    game = tris()
    game.play((0,0))
    game.play('A2')
    game.play('C1')
    game.play('C2')
    game.play('B1')
    print('\n\n')
    game.show_table()
    print('\n\n')
    print(game.check_end())