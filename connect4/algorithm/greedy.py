import random as r

def greedy(game):
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
                    if not player == 0:
                        #add bais for blank adiacente cell that can be filled in future
                        count[player] += 0.4*player
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

class test:
    def __init__(self,game):
        self.row_number = game.row
        self.column_number = game.column
        self.board = game.board
        self.opponent = game.current_player * -1
        self.number_to_win = game.win_number
        self.box_to_check = []

    def check_option(self):
        for x in range(1,self.column_number+1):
            prev = True
            for y in range(1,self.row_number+1):
                if self.board[(x,y)] == 0 and prev == True:
                    self.box_to_check.append((x,y))
                    prev = False
    
    def evaluate_combination(self,box):
        '''
        from given blank box calculate the 'value' of the box.
        start from box and go back to check if there i sequence
        score logic sould look like this:
            - if there is not possibility to end a winning sequence 0 point
            - 
        '''
        offset_to_check = list(range(-(self.number_to_win-1),self.number_to_win)) #ex. [-3,-2,-1,0,1,2,3]
        max_x = self.column_number
        min_x = 1
        max_y = self.row_number
        min_y = 1
        direction_list = [ #direction to check
                        [+1,0],     #vertical
                        [0,+1],     #horizontal
                        [+1,+1],    #from dx to sx oblique
                        [+1,-1]]    #from sx to dx oblique
        x = box[0]
        y = box[1]
        combination_list = [] #ex. [[1,1,0,-1,...],....]
        for direction in direction_list:
            dir_x = direction[0]
            dir_y = direction[1]
            combination = []
            for offset in offset_to_check:
                #calculate the offset direction
                off_x = x+(offset*dir_x)    #ex. 1+(+3*+1) == 4
                off_y = y+(offset*dir_y)    #ex. 4+(+3*-1) == 1
                
                #skip loop when offset x/y is out of the board
                if not max_x >= off_x >= min_x: #ex. 7 >= 4 >= 1 == True
                    continue
                if not max_y >= off_y >= min_y: #ex. 7 >= 0 >= 1 == False
                    continue

                off_value = self.board[(off_x,off_y)]
                combination.append(off_value)
            combination_list.append(combination)

        for combination in combination_list:
            score_list = [] #ex. [(score,possible streak,pawn treat),()]
            player = None #the current player that are counting
            consecutive = 0 #a int that store the number of pawn not interupt with a blank spot, if = 3 is a winnig move
            consecutive_list = []
            score = 0 #the n. of consecutive pawn of the player (not counting blank spot)
            possible_sequence_len = 0 #a count to see if the sequence can end with a win number
            blank_sequence = 0 #count the blank spot to add to possibile_sequence, and ad 0.1 to 'count' how much direction have to continue the sequence (_XX_) = 4.2 - (XX__) = 4.1
            for n, value in enumerate(combination,offset_to_check[0]):
                if value == 0:
                    consecutive_list.append(consecutive)
                    consecutive = 0
                    if blank_sequence == 0:
                        blank_sequence += 1.1
                    else:
                        blank_sequence += 1
                elif player == None:
                    player = value
                    score = player
                    possible_sequence_len = blank_sequence+1
                    blank_sequence = 0
                    consecutive = 1
                elif value == player:
                    score += player
                    possible_sequence_len += blank_sequence + 1
                    blank_sequence = 0
                    consecutive +=1
                else:
                    consecutive_list.append(consecutive)
                    possible_sequence_len += blank_sequence
                    score_list.append((max(consecutive_list),score,round(possible_sequence_len,2)))
                    possible_sequence_len = 1 + blank_sequence
                    blank_sequence = 0
                    player = value
                    score = player
                    consecutive_list = []
                    consecutive = 1
            possible_sequence_len += blank_sequence
            consecutive_list.append(consecutive)
            score_list.append((max(consecutive_list),score,round(possible_sequence_len,2)))
            possible_sequence_len = 1 + blank_sequence
        
        sorted_score_list = sorted(score_list, key=lambda x: (x[0], x[1], x[2]),reverse=True)
        best_score = sorted_score_list[0]
        return(best_score)
    
    def evaluate_options(self):
        self.check_option()
        best = (0,0,0)
        best_x = 1
        for box in self.box_to_check:
            box_score = self.evaluate_combination(box=box)
            box_consecutive = box_score[0]
            box_sequence = box_score[1]
            box_future = box_score[2]
            if box_future < self.number_to_win:
                continue
            if abs(box_consecutive) == self.number_to_win-1:
                if box_sequence*self.opponent < 0:
                    return box[0]
            if box_future > best[2]:
                best_x = box[0]
                best = box_score
        return best_x
            

        




                

            

        


        
