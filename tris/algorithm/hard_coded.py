import random as r

def random(game):
    options = game.legit_move
    return r.choice(options)