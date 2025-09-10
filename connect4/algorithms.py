from random import choice

def random(game):
    list = game.legit_move

    r = choice(list)
    return r

def v0(game):
    legit_move = game.legit_move
    board = game.board
    column = game.column
    row = game.row
    n_to_win = game.win_number

    box_to_check = []
    for x in range(1,column+1):
        prev = True
        for y in range(1,row+1):
            if board[(x,y)] == 0 and prev == True:
                box_to_check.append((x,y))
                prev = False

    for box in box_to_check:
        x = box[0]
        y = box[1]
        #vertical
        count = 1
        player = 0
        for n in range(n_to_win,0,-1):
            if y-n >0:
                value = board[(x,y-n)]
            else:
                break
            if value == player:
                count += 1
            else:
                player = value
                count = 1
            if count >= n_to_win-1 and player!=0:
                return x
        
        #orrizontal (sx+dx)
        count = 1
        player = 0
        for n in range(n_to_win-1,0,-1): #sx
            if x-n > 0:
                value = board[(x-n,y)]
            else:
                break
            if value == player:
                count += 1
            else:
                player = value
                count = 1
            if count >= n_to_win-1 and player!=0:
                return x
        
        for n in range(1,n_to_win):
            if x+n <= column:
                value = board[(x+n,y)]
            else:
                break
            if value == player:
                count += 1
            else:
                player = value
                count = 1
            if count >= n_to_win-1 and player!=0:
                return x
            
    return choice(legit_move) #add prefer in the middle


            


            
