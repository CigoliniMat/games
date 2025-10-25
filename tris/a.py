from engine import tris
from learning.RL import Qlearning
from algorithm.hard_coded import random

def gamesimulator(n=1):

    game = tris()
    cpu1 = Qlearning()
    cpu2 = Qlearning()

    while True:
        if game.current_player == 1:
            move = cpu1.choose(game)
        else:
            move = cpu2.choose(game)

        game.play(move)

        end, winner = game.check_end()


        if end:
            break
        
    #winner is 1, -1 or 0 for draw
    cpu2.end(-1*winner)
    cpu1.end(1*winner)

if __name__ == '__main__':
    for i in range(100000):
        gamesimulator()
