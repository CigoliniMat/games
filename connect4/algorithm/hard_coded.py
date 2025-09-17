from random import choice
from time import sleep
row_number = int
column_number = int
number_to_win = 4
box_to_check = []
board = {}
legit_move = []
my_pawn = 1
opponent_pawn = -1

def _get_playable_box():
    '''
    input = {(x,y):player,(1,1):0,....} 0 == blank box, -1/+1 = player pawn
    by given board get a list of playable coordinate
    output = [(x,y),(1,2),...]

    for each column of the board strat from the botton and watch if the value is 0
    add the coordinate to the list, then pass to next column
    '''
    playable_box = []
    for x in range(1,column_number+1):
        for y in range(1,row_number+1):
            if board[(x,y)] == 0:
                playable_box.append((x,y))
                break
    return(playable_box)

def _winning_move(move):
    '''
    board = {(x,y):player,(1,1):0,....} 0 == blank box, -1/+1 = player pawn
    move = (x,y) coordinate of the table

    for the given move check if there is a winning move
    
    output1 = True/false
    output2 = pawn value (to check what player are winning) 
    '''
    x = move[0]
    y = move[1]
    offset_to_check = list(range(1,number_to_win)) #offset from teh given move to watch ex. [1,2,3]
    combination_direction = [
                            (0,1),#horizontal
                            (1,0),#vertical
                            (1,1),#from dx to sx oblique
                            (1,-1)#from sx to dx oblique
                            ]
    player_score = {1:0,-1:0}
    for combination in combination_direction: #the direction to watch (vertical, horizontal,...)
        player = 0 #the current player count
        count = 0 #the focus consecutive pawn counter
        for off_direction in (-1,1): #the direction of the offset (-1 vs dx, +1 vs dx) from the playable box
            for offset in offset_to_check:
                off_x = x + (combination[0]*off_direction*offset) #ex. 1 + (1*-1*3) == 1+(-3) == -2
                off_y = y + (combination[1]*off_direction*offset) #ex. 2 + (0*1*3) == 2+(0) == 2
                #verify of the offset box is in the board range
                if not column_number >= off_x >= 1:
                    continue
                if not row_number >= off_y >= 1:
                    continue

                off_value = board[(off_x,off_y)]
                if off_value == 0:                          #if found a void block stop watching in that direction
                    break
                elif player == 0:                           #if is the first pawn finded in the sequence
                    player = off_value
                    count += 1
                elif off_value == player:                   #if the prev pawn == this pawn add 1 to counter
                    count += 1
                elif offset == 1 and off_direction ==1:     #when switch from dx to sx from the playable box
                    if count > player_score[player]:
                        player_score[player] = count
                    player = off_value
                    count = 1
                else:                                       #if found a different pawn stop watching in that direction
                    break
            if player != 0 and count > player_score[player]:
                        player_score[player] = count
            
    if player_score[my_pawn]+1 >= number_to_win: #priotaize my win for obv reason
        return True, my_pawn
    elif player_score[opponent_pawn]+1 >= number_to_win:
        return True, opponent_pawn
    else:
        return False, 0

#_basic_move_score

def extra_basic(game):
    global row_number
    global column_number
    global board
    global number_to_win
    global legit_move
    global my_pawn
    global opponent_pawn

    row_number = game.row
    column_number = game.column
    board = game.board
    number_to_win = game.win_number
    legit_move = game.legit_move
    my_pawn = game.current_player
    opponent_pawn = my_pawn*-1

    box_to_check = _get_playable_box()
    stopping_x = None
    for box in box_to_check:
        winning, player = _winning_move(box)
        if winning:
            if player == my_pawn:
                return box[0]
            else:
                stopping_x = box[0]
    
    if not stopping_x == None:
        return stopping_x
    else:
        return choice(legit_move)

    

    



