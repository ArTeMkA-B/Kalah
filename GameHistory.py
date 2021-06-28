from Kalah import *


class MoveInfo:
    def __init__(self, id, move, state):
        self.player_id = id
        self.move = move
        self.state = state


class GameHistory:
    def __init__(self):
        self.moves_history = []

    def SaveMove(self, move_info):
        self.moves_history.append(move_info)

    def DeleteLastMove(self):
        self.moves_history.pop()

    def GetLastActivePlayer(self):
        assert len(self.moves_history) > 0, 'Empty history of moves'
        return self.moves_history[-1].player_id

    def GetLastState(self):
        assert len(self.moves_history) > 0, 'Empty history of moves'
        return self.moves_history[-1].state


