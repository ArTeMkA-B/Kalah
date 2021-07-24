from Kalah import *
from random import randint


class GoodBot:
    def __init__(self, id, log=False):
        self.id = id
        self.kalah = Kalah()
        self.score = 0
        self.all_moves = {}
        self.diff = 0
        self.log = log

    def ChooseMove(self, kalah:Kalah):
        moves = kalah.GetPossibleMoves()
        if len(moves) == 1:
            return [move for move in moves]

        self.all_moves = {}
        self.kalah = kalah
        self.diff = kalah.GetScore(self.id) - kalah.GetScore((self.id + 1) % 2)

        for move in moves:
            self.ImitateMove(move, [], False)
        all_moves = dict(sorted(self.all_moves.items(), key=lambda x: x[1], reverse=True))
        sequence = list(all_moves.keys())[0]
        best_moves = [move for move in list(all_moves.keys()) if all_moves.get(move) == all_moves.get(sequence)]
        chosen_move = self.ToArray(best_moves[randint(0, len(best_moves) - 1)])
        if self.log:
            # print('(GB)', self.kalah.state, ':', best_moves, '=>', chosen_move)
            print("GoodBot moves:", chosen_move)
        return chosen_move

    def ToString(self, array):
        result = ""
        for i in array:
            result += str(i) + " "
        return result

    def ToArray(self, string):
        return [int(s) for s in string.split()]

    def ImitateMove(self, move, moves_sequence, can_exit):
        last_player = self.kalah.active_player
        self.kalah.MakeMove(move)
        need_pop = False
        if not can_exit:
            need_pop = True
            moves_sequence.append(move)
        if self.kalah.IsGameOver() or (self.kalah.active_player != last_player and can_exit):
            if self.ToString(moves_sequence) not in self.all_moves:
                self.all_moves[self.ToString(moves_sequence)] = self.kalah.GetScore(self.id) - self.kalah.GetScore((self.id + 1) % 2) - self.diff
            else:
                self.all_moves[self.ToString(moves_sequence)] = min(self.all_moves[self.ToString(moves_sequence)], self.kalah.GetScore(self.id) - self.kalah.GetScore((self.id + 1) % 2) - self.diff)
            self.kalah.UndoLastMove()
            if need_pop:
                moves_sequence.pop()
            return
        if self.kalah.active_player != last_player:
            can_exit = True
        possible_moves = self.kalah.GetPossibleMoves()
        for mov in possible_moves:
            self.ImitateMove(mov, moves_sequence, can_exit)
        self.kalah.UndoLastMove()
        if need_pop:
            moves_sequence.pop()
