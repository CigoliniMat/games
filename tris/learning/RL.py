import random
import json
import pickle
import os.path

Qtable_path = 'tris/learning/Qtable.pkl'
base_point = 10

class Qlearning:
    def __init__(self):
        if os.path.isfile(Qtable_path):
            with open(Qtable_path, 'rb') as f:
                self.Qtable = pickle.load(f)
                f.close()
        else:
            self.Qtable = {}
        self.history = []

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
            choice = random.choice(legit_move)
        else:
            options = []
            weights = []
            for option in self.Qtable[state]:
                weight = self.Qtable[state][option]
                if weight <= 0:
                    continue
                options.append(option)
                weights.append(weight)
            if len(options) == 0:
                choice = random.choice(legit_move)
            else:
                choice = random.choices(options,weights)[0]

        self.history.append((state,choice))

        return choice

    def end(self,reward):
        if reward == 0:
            reward = -0.5
        for n,record in enumerate(self.history):
            n += 1
            state = record[0]
            choice = record[1]

            current_value = self.Qtable[state][choice]
            self.Qtable[state][choice] = current_value + (n*reward)

        with open(Qtable_path, 'wb') as f:
            pickle.dump(self.Qtable,f)
            f.close()


def read_pickle():
    with open(Qtable_path, 'rb') as f:
                Qtable = pickle.load(f)
                f.close()
    for i in Qtable:
        print(i)

def choose(game):
        with open(Qtable_path, 'rb') as f:
            Qtable = pickle.load(f)
            f.close()
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
        if not state in Qtable:
            options = {}
            for move in legit_move:
                options[move] = base_point
            Qtable[state] = options
            choice = random.choice(legit_move)
        else:
            options = []
            weights = []
            for option in Qtable[state]:
                weight = Qtable[state][option]
                if weight <= 0:
                    continue
                options.append(option)
                weights.append(weight)
            if len(options) == 0:
                choice = random.choice(legit_move)
            else:
                choice = random.choices(options,weights)[0]

        return choice

if __name__ == '__main__':
    read_pickle()
