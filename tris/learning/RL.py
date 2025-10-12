import random
import json
import os.path

Qtable_path = 'tris/learning/Qtable.json'
base_point = 1

class Qlearning:
    def __init__(self):
        if os.path.isfile(Qtable_path):
            with open(Qtable_path,'r+') as f:
                self.Qtable = json.load(f)
        else:
            self.Qtable = {}
        self.history = {}

    def choose(self,game):
        legit_move = game.legit_move
        board = game.board
        linear_board = []

        for row in board:
            for box in row:
                # if it isn't the n. 1 player reverse the pawn value to mantaine the same board
                if game.current_player == -1:
                    box = box*-1
                linear_board.append(box) 

        state = tuple(linear_board)
        if not state in self.Qtable:
            options = {}
            for move in legit_move:
                options[move] = base_point
            self.Qtable[state] = options


