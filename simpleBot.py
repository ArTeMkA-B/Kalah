from Kalah import *
from random import randint


class SimpleBot:
    def __init__(self, id):
        self.id = id  # 0 or 1

    def ChooseMove(self, state, moves, kalah_index):
        if len(moves) == 1:
            return moves[0]

        # find move with eating max opponent chips
        limit = 13 if self.id == 0 else 20
        best_prize = 0
        best_move = -1
        for move in moves:
            last_chip_index = ((move + state[move]) % 14 + (move + state[move]) // limit) % 14
            if state[last_chip_index] == 0:
                prize = state[12 - last_chip_index] + 1
                if prize > best_prize:
                    best_prize = prize
                    best_move = move

        # find move with last chip in kalah to make move again
        best_moves = [move for move in moves if self.GetLastChipIndex(move, state[move]) == kalah_index]
        if len(best_moves):
            best_moves = sorted(best_moves, reverse=True)
            return best_moves[0] if best_moves[0] > best_move else best_move
        else:
            return moves[randint(0, len(moves) - 1)]

    def GetLastChipIndex(self, start_index, chips_count):
        offset = 7 if self.id == 1 else 0
        return ((start_index + chips_count) % 14 + (start_index + chips_count - offset) // 13) % 14
