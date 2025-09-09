from random import choice
import os
from colorama import Fore, Style

class connect4:
    row = 6
    column = 7
    win_number = 4
    player_dict = {None:'blank',#' '
                   0:'player1',#X
                   1:'player2/pc'#O
                   }

    def __init__(self):
        self.current_player = choice([0,1])
        self.move_number = 0
        self.board = {}
        for x in range(1,self.column+1):
            for y in range(1,self.row+1):
                self.board[x,y] = None
        self.legit_move = list(range(1,self.column+1))
    
    def clean_terminal(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    
    def show_table(self):
        player_mark = {None:' ',#blank
                        0:'X',#player1
                        1:'O'#player2/pc
                        }
        self.clean_terminal()

        if self.move_number == 0:
            print(f'Welcome to connect{self.win_number},')
            print(f'choose a column to fill the button row, the first that connect{self.win_number} pawn Win!')
            print(f'\nthe {self.player_dict[self.current_player]} start!\n')
        r_row = reversed(list(range(1,self.row+1)))
        for y in r_row:
            print(' '*3,end='')
            for x in range(1,self.column+1):
                print('| ',end='')

                value = self.board[(x,y)]
                if value == 0:
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
            if self.board[(column,y)] == None:
                self.board[(column,y)] = self.current_player
                if y == self.row:
                    self.legit_move.remove(column)
                return
        return False
    
    def check_end(self):
        # draw
        if len(self.legit_move) == 0:
            return True, None
        
        for y in range(1,self.row+1):
            for x in range(1,self.column+1): #for each block of the board
                value = self.board[(x,y)]
                
                if value == None:
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


        return False, None
         
    def switch_player(self):
        if self.current_player == 0:
            self.current_player = 1
        else:
            self.current_player = 0
            
    def terminal_game(self):
        while True:
            self.show_table()
            try:
                choose = int(input(f'\n{self.player_dict[self.current_player]} choose one column: '))
            except ValueError:
                print('Insert a valid number! ')
                input("Press ENTER to retry...")
                continue

            if choose not in self.legit_move:
                print('Insert a valid column! ')
                input("Press ENTER to retry...")
                continue
            self.insert_pawn(choose)
            self.move_number +=1
            end, who = self.check_end()
            if end:
                self.show_table()
                if who == None:
                    print("It's a Draw!")
                else:
                    print(f'\n{self.player_dict[who]} Win!')
                break

            self.switch_player()

if __name__ == '__main__':
    pass
    a = connect4()
    a.terminal_game()



