from Kalah import *


class RealPlayer:
    def __init__(self, id, log=False):
        self.id = id
        self.log = log

    def ChooseMove(self, kalah):
        possible_moves = kalah.GetPossibleMoves()
        print("Your possible moves:", possible_moves)
        chosen_move = int(input("Chosen move:"))
        while chosen_move not in possible_moves:
            print("Impossible move! Try again.")
            chosen_move = int(input("Chosen move: "))
        return [chosen_move]
