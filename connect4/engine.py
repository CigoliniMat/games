from random import choice
import os
from colorama import Fore, Style

class connect4:
    row = 6
    column = 7
    win_number = 4
    player_dict = {0:'blank',#' '
                   -1:'player1',#X
                   1:'player2/pc'#O
                   }

    def __init__(self):
        self.current_player = choice([-1,1])
        self.move_number = 0
        self.board = {}
        for x in range(1,self.column+1):
            for y in range(1,self.row+1):
                self.board[x,y] = 0
        self.legit_move = list(range(1,self.column+1))
    
    def _clean_terminal(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    
    def switch_player(self):
        if self.current_player == 1:
            self.current_player = -1
        else:
            self.current_player = 1

    def show_table(self):
        player_mark = {0:' ',#blank
                        -1:'X',#player1
                        1:'O'#player2/pc
                        }
        
        r_row = reversed(list(range(1,self.row+1)))
        for y in r_row:
            print(' '*3,end='')
            for x in range(1,self.column+1):
                print('| ',end='')

                value = self.board[(x,y)]
                if value == 1:
                    print(Fore.RED+f'{player_mark[value]} ',end='')
                else:
                    print(Fore.BLUE+f'{player_mark[value]} ',end='')
                print(Style.RESET_ALL,end='')
            print('|')
            print(' '*3,end='')
            for x in range(1,self.column+1):
                print(f'+---',end='')
            print('+')

        print(' '*3,end='')
        for x in range(1,self.column+1):
            print('| ',end='')
            if x in self.legit_move:
                print(Style.BRIGHT,end='')
                print(f'{x} ',end='')
            else:
                print(Fore.LIGHTBLACK_EX,end='')
                print(f'{x}*',end='')
            print(Style.RESET_ALL,end='')
        print('|')

    def insert_pawn(self,column):
        for y in range(1,self.row+1):
            if self.board[(column,y)] == 0:
                self.board[(column,y)] = self.current_player
                if y == self.row:
                    self.legit_move.remove(column)
                self.move_number += 1
                return
        
    def check_end(self):
        
        for y in range(1,self.row+1):
            for x in range(1,self.column+1): #for each block of the board
                value = self.board[(x,y)]
                
                if value == 0:
                    continue
                count = {'vertical':1,
                         'orrizontal':1,
                         'dx_oblique':1,
                         'sx_oblique':1}
                out_up = False
                out_dx = False
                out_sx = False
                for n in range(1,self.win_number):#1 to 3 (the 0 is the start value)

                    if y+self.win_number-1 > self.row:
                        out_up = True
                    else:
                        out_up = False

                    if x+self.win_number-1 > self.column:
                        out_dx = True
                    else:
                        out_dx = False
                    
                    if x-self.win_number+1 < 1:
                        out_sx = True
                    else:
                        out_sx = False

                    if not out_up:
                        if self.board[(x,y+n)] == value:
                            count['vertical'] += 1
                    
                    if not out_dx:
                        if self.board[(x+n,y)] == value:
                            count['orrizontal'] += 1
                    
                    if not out_up and not out_dx:
                        if self.board[(x+n,y+n)] == value:
                            count['dx_oblique'] += 1
                    
                    if not out_up and not out_sx:
                        if self.board[(x-n,y+n)] == value:
                            count['sx_oblique'] += 1
                for c in count:
                    if count[c] >= self.win_number:
                        return True, value
                    count[c] = 1

        # draw
        if len(self.legit_move) == 0:
            return True, 0

        return False, None

if __name__ == '__main__':
    pass



