import random as r

def random(game):
    options = game.legit_move

    return r.choice(options)

def random_plus(game):
    options = game.legit_move
    column = game.column

    if len(options) == 1:
        return options[0]
    
    if column%2 ==0:
        center = column/2
    else:
        center = (column+1)/2
    weights = []
    for number in options:
        p = 1/(abs(number-center)+1)**2
        weights.append(p)

    return r.choices(options,weights=weights)[0]

def best_placement(game):
    options = game.legit_move
    column = game.column
    if column%2 ==0:
        center = column/2
    else:
        center = (column+1)/2

    near_factor = column
    nearest_n = 0
    r.shuffle(options)
    for n in options:
        value = abs(n-center)
        if value == 0:
            return(n)
        if value < near_factor:
            nearest_n = n
            near_factor = value
    
    return nearest_n

    


if __name__ == '__main__':
    pass
    
    
    