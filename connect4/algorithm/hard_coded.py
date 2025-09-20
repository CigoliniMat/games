from random import choice, shuffle
from time import sleep
row_number = int
column_number = int
number_to_win = int
box_to_check = list
board = dict
legit_move = list
my_pawn = int
opponent_pawn = int

def _update_game_info(game):
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

def _winning_move(move, priority):
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
            
    if player_score[priority]+1 >= number_to_win: #priotaize my win for obv reason
        return True, priority
    elif player_score[priority*-1]+1 >= number_to_win:
        return True, priority*-1
    else:
        return False, 0

def _basic_move_score(move):
    '''
    copy of winning move but insteand of say only if the move is a winning move say also a number of consecutive pawn
    
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
    score_list = []
    for combination in combination_direction: #the direction to watch (vertical, horizontal,...)
        player = 0 #the current player count
        count = 0 #the focus consecutive pawn counter
        streak = True
        treath = 1 #the number of possibile combination (if<4 no one can close a winnig combination)
        for off_direction in (-1,1): #the direction of the offset (-1 vs dx, +1 vs dx) from the playable box
            streak = True
            for offset in offset_to_check:
                off_x = x + (combination[0]*off_direction*offset) #ex. 1+(0*-1*1) == 1+(0) == 1
                off_y = y + (combination[1]*off_direction*offset) #ex. 2+(1*-1*3) == 2+(-3) == -1
                #verify of the offset box is in the board range
                if not column_number >= off_x >= 1:
                    break
                if not row_number >= off_y >= 1:
                    break
                off_value = board[(off_x,off_y)]
                if off_value == 0:  #if found a void block add a treath point and stop strek counting
                    treath += 1
                    streak = False
                elif player == 0:   #if is the first pawn finded in the sequence
                    player = off_value
                    if streak:
                        count += 1
                    treath +=1
                elif off_value == player:   #if the prev pawn == this pawn add 1 to counter
                    if streak:
                        count += 1
                    treath +=1
                elif offset == 1 and off_direction ==1: #when switch from dx to sx from the playable box
                    streak = True
                    if count > player_score[player]:
                        score_list.append({player:(count,treath)})
                    player = off_value
                    count = 1
                    treath = 1
                    treath += 1
                else:   #if found a different pawn stop watching in that direction
                    break
            if player != 0 and count > player_score[player]:
                score_list.append({player:(count,treath)})

    for score in score_list:
        player = list(score.keys())[0]
        point = score[player][0]
        treath = score[player][1]

        if treath >= number_to_win and point > player_score[player]:
            player_score[player] = point
    
    return player_score

def _move_score(move):
    '''
    equal to basic_move but add a check if the move make opponent win
    '''
    y = move[1]
    basic_score = _basic_move_score(move)
    if y >= row_number:
        return basic_score
    for player in basic_score:
        if basic_score[player]+1 >= number_to_win:
            return basic_score
    move_plus = (move[0],y+1)
    winning, player = _winning_move(move_plus, opponent_pawn)
    if not winning:
        return basic_score
    if player == opponent_pawn:
        return({1:-2,-1:-2})
    else:
        return({1:-1,-1:-1})


def extra_basic(game):
    _update_game_info(game)

    box_to_check = _get_playable_box()
    stopping_x = None
    for box in box_to_check:
        winning, player = _winning_move(box, my_pawn)
        if winning:
            if player == my_pawn:
                return box[0]
            else:
                stopping_x = box[0]
    
    if not stopping_x == None:
        return stopping_x
    else:
        return choice(legit_move)

def basic(game):
    _update_game_info(game)

    box_to_check = _get_playable_box()
    x_pool = []
    best_score = 0
    for box in box_to_check:
        x = box[0]
        score_card = _basic_move_score(box)
        my_point = score_card[my_pawn]
        opponent_point = score_card[opponent_pawn]
        if my_point+1 >= number_to_win:
            return x
        for n in (my_point,opponent_point):
            if n > best_score:
                x_pool.clear()
                best_score = n
            if n == best_score:
                x_pool.append(x)
    if len(x_pool) == 1:
        return x_pool[0]
    
    shuffle(x_pool)
    if column_number%2 ==0:
        middle = column_number/2
    else:
        middle = (column_number+1)/2
    nearest_x = 0
    near_factor = column_number
    for x in x_pool:
        value = abs(x-middle)
        if value == 0:
            return x
        if value < near_factor:
            nearest_x = x
            near_factor = value
    
    return nearest_x

def medium(game):
    '''
    a cpoy of basic but check if the move make win the opponent
    '''
    _update_game_info(game)

    box_to_check = _get_playable_box()
    x_pool = []
    best_score = -999999999
    for box in box_to_check:
        x = box[0]
        score_card = _move_score(box)
        my_point = score_card[my_pawn]
        opponent_point = score_card[opponent_pawn]
        if my_point+1 >= number_to_win:
            return x
        for n in (my_point,opponent_point):
            if n > best_score:
                x_pool.clear()
                best_score = n
            if n == best_score:
                x_pool.append(x)
    
    shuffle(x_pool)
    if column_number%2 ==0:
        middle = column_number/2
    else:
        middle = (column_number+1)/2
    nearest_x = -999999999
    near_factor = column_number
    for x in x_pool:
        value = abs(x-middle)
        if value == 0:
            return x
        if value < near_factor:
            nearest_x = x
            near_factor = value
    return nearest_x

if __name__ == '__main__':
    board = {(1, 1): 0, (1, 2): 0, (1, 3): 0, (1, 4): 0, (1, 5): 0, (1, 6): 0,
             (2, 1): 0, (2, 2): 0, (2, 3): 0, (2, 4): 0, (2, 5): 0, (2, 6): 0,
             (3, 1): 1, (3, 2): 0, (3, 3): 0, (3, 4): 0, (3, 5): 0, (3, 6): 0,
             (4, 1): 1, (4, 2): 0, (4, 3): 0, (4, 4): 0, (4, 5): 0, (4, 6): 0,
             (5, 1): 0, (5, 2): 0, (5, 3): 0, (5, 4): 0, (5, 5): 0, (5, 6): 0,
             (6, 1): 0, (6, 2): 0, (6, 3): 0, (6, 4): 0, (6, 5): 0, (6, 6): 0,
             (7, 1): -1, (7, 2): -1, (7, 3): -1, (7, 4): 1, (7, 5): 1, (7, 6): 0}
    move = (1,1)
    number_to_win = 4
    column_number = 7
    row_number = 6

    r = _basic_move_score(move)
    print(r)
