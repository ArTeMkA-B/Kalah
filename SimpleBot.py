from random import randint
from Kalah import *


class SimpleBot:
    def __init__(self, id, log=False):
        self.id = id  # 0 or 1
        self.score = 72
        self.log = log


    def ChooseMove(self, kalah:Kalah):

        state = kalah.state
        moves = kalah.GetPossibleMoves()
        kalah_index = kalah.GetKalahIndex()

        if len(moves) == 1:
            return [moves[0]]

        """"# find moves with eating opponent chips
        limit = 13 if self.id == 0 else 20
        eat_moves = []
        for move in moves:
            last_chip_index = ((move + state[move]) % 14 + (move + state[move]) // limit) % 14
            if state[last_chip_index] == 0 and ((self.id == 0 and last_chip_index >= 0 and last_chip_index < 6) or
                                                (self.id == 1 and last_chip_index >= 7 and last_chip_index < 13)):
                prize = state[12 - last_chip_index] + 1 + int(last_chip_index <= move)
                eat_moves.append(move)
        eat_moves = sorted(eat_moves, reverse=True)"""

        # find moves with last chip in kalah to make move again
        again_moves = [move for move in moves if self.GetLastChipIndex(move, state[move]) == kalah_index]
        if len(again_moves):
            again_moves = sorted(again_moves, reverse=True)

        # analyze not_again moves
        not_again_moves = [move for move in moves if move not in again_moves]
        scores = {}
        scores_before = kalah.GetScore(self.id) - kalah.GetScore((self.id + 1) % 2)
        for move in not_again_moves:
            kalah.MakeMove(move)
            if kalah.IsEnd:
                self.score = kalah.GetScore(self.id) - kalah.GetScore((self.id + 1) % 2)
            else:
                self.CalculateScore(kalah)
            kalah.UndoLastMove()
            scores[move] = self.score - scores_before
            self.score = 72
        scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        not_again_moves = list(scores.keys())

        """moves_count = len(scores_moves) + len(again_moves)
        opponent_start = 0 if self.id == 1 else 7
        possible_opponent_kalah = sum(kalah.state[opponent_start:opponent_start+6]) + kalah.GetScore((self.id + 1) % 2)
        count = 0
        if len(scores_moves):
            for move in again_moves:
                if move > scores_moves[0]:
                    break
                count += 1"""

        if len(again_moves) > 0:
            if len(not_again_moves) == 0 or again_moves[0] > not_again_moves[0]:  #and (len(moves) > 3 or kalah.GetScore(self.id) >= 36):
                if self.log:
                    print('(SB)', kalah.state, ':', moves, '=>', [again_moves[0]])
                return [again_moves[0]]
        best_moves = [move for move in not_again_moves if scores.get(move) == scores.get(not_again_moves[0])]
        chosen_move = [best_moves[randint(0, len(best_moves) - 1)]]
        if self.log:
            print('(SB)', kalah.state, ':', moves, '=>', chosen_move)
        return chosen_move

        """ if len(again_moves) > 0:
            if len(eat_moves) == 0 or again_moves[0] > eat_moves[0]:
                return again_moves[0]
        if len(eat_moves) > 0:
            for move in eat_moves:
                if scores.get(move) != None:
                    if scores.get(move) > 0:
                        return move
        return list(scores.keys())[0]  # add random """

    def CalculateScore(self, kalah:Kalah):
        for move in kalah.GetPossibleMoves():
            kalah.MakeMove(move)
            if kalah.active_player != self.id:
                self.CalculateScore(kalah)
            else:
                self.score = min(self.score, kalah.GetScore(self.id) - kalah.GetScore((self.id + 1) % 2))
            kalah.UndoLastMove()

    def GetLastChipIndex(self, start_index, chips_count):
        offset = 7 if self.id == 1 else 0
        return ((start_index + chips_count) % 14 + (start_index + chips_count - offset) // 13) % 14
