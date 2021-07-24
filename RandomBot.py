from Kalah import *
from random import randint

class RandomBot:
    def __init__(self, id, log=False):
        self.id = id
        self.log = log

    def ChooseMove(self, kalah: Kalah):
        possible_moves = kalah.GetPossibleMoves()
        chosen_move = [possible_moves[randint(0, len(possible_moves) - 1)]]
        if self.log:
            print('(RB)', kalah.state, ':', possible_moves, '=>', chosen_move)
        return chosen_move
