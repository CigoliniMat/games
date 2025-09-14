import random as r

def basic_greedy(game):
    row_number = game.row
    column_number = game.column
    board = game.board
    number_to_win = game.win_number
    box_to_check = []
    option_list = {}

    def check_combination(x_direction,y_direction):
        '''
        by given board position and direction to check see if there is a sequence of equal pawn

        '''
        #list of number of sequence to check
        range_to_check = list(range(1,number_to_win))
        count = {1:0,-1:0} #positive number are pc pawn, negative human pawn
        player = 0
        
        for direction in [1,-1]: #reverse the direction after the first loop
            x_direction = x_direction*direction
            y_direction = y_direction*direction
            for offset in range_to_check:
                pawn_x = x+(offset*x_direction)
                pawn_y = y+(offset*y_direction)
                if  0 >= pawn_x or pawn_x > column_number:
                    continue
                if 0 >= pawn_y or pawn_y > row_number:
                    continue

                pawn_value = board[(pawn_x,pawn_y)]
                #if there is blank box got to next box
                if pawn_value == 0:
                    continue
                #if player=0 (is the first pwan finded) or pawn = previus pawn
                elif player == 0 or pawn_value == player:
                    player = pawn_value
                    count[pawn_value] += pawn_value
                #if when switch offset direction find a new pawn restart counting
                elif offset == 1:
                    player = pawn_value
                    count[pawn_value] = pawn_value
                else:
                    break

        max_count = 0
        for player in count:
            value = count[player]
            #if there is a winnig move prioritize that
            if value >= number_to_win-1:
                max_count = 100
            #add bais: +0.5 aggressive(prefer continue his sequnce), -0.5 passive (prefer stop the opponent), 0 neutral
            #I think the best is passive because in aggressive mode he can't know if there is enough space to conclude the sequence
            #in test vs himself this value doesn't change much
            elif value > 0:
                value += r.choice([-0.5,0,0.5])

            value = abs(value)
            if value > max_count:
                max_count = value
        return max_count

    #make a list of the playable box
    for x in range(1,column_number+1):
        prev = True
        for y in range(1,row_number+1):
            if board[(x,y)] == 0 and prev == True:
                box_to_check.append((x,y))
                prev = False
    
    for box in box_to_check:
        max_sequence = 0
        x = box[0]
        y = box[1]
        #vertical offset
        sequence = check_combination(x_direction=0,y_direction=-1)
        if sequence >= max_sequence:
            max_sequence = sequence
        #orizzontal sequence
        sequence = check_combination(x_direction=-1,y_direction=0)
        if sequence >= max_sequence:
            max_sequence = sequence
        #dx oblique sequence
        sequence = check_combination(x_direction=-1,y_direction=-1)
        if sequence >= max_sequence:
            max_sequence = sequence
        #sx oblique sequence
        sequence = check_combination(x_direction=-1,y_direction=1)
        if sequence >= max_sequence:
            max_sequence = sequence
        #add center bias
        option_list[x] = max_sequence
    
    max_sequence = 0
    option_pool = []
    for key in option_list:
        value = option_list[key]
        if value == max_sequence:
            option_pool.append(key)
        elif value > max_sequence:
            option_pool = [key]
            max_sequence = value
    if len(option_pool) == 1:
        return option_pool[0]
    
    if column_number%2 ==0:
        center = column_number/2
    else:
        center = (column_number+1)/2
    weights = []

    for number in option_pool:
        p = 1/(abs(number-center)+1)**2
        weights.append(p)

    return r.choices(option_pool,weights=weights)[0]