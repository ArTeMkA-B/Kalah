from GameHistory import *
from copy import deepcopy

class Kalah:
    def __init__(self):
        self.state = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
        self.cells_number = 14
        self.active_player = 0  # players: 0 and 1
        self.kalah0_index = 6
        self.kalah1_index = 13
        self.IsEnd = False
        self.winner = -1
        self.history = GameHistory()

    def GetKalahIndex(self):
        return self.kalah0_index if self.active_player == 0 else self.kalah1_index

    def GetPossibleMoves(self):
        start_index = 0 if self.active_player == 0 else 7
        possible_moves = [i for i in range(start_index, start_index+6) if self.state[i] > 0]
        return possible_moves

    def PrintState(self):
        state_str = ''
        for i in range(self.cells_number // 2 - 1, -1, -1):
            state_str += str(self.state[i]) + ' '  # first player
        state_str += '\n  '
        for i in range(self.cells_number // 2, self.cells_number):
            state_str += str(self.state[i]) + ' '  # second player
        print(state_str)

    def IsOwnCell(self, cell_index):
        assert cell_index >= 0 and cell_index < self.cells_number, 'Invalid cell index ' + str(cell_index)
        return self.active_player == 0 and cell_index <= 6 or self.active_player == 1 and cell_index >= 7

    def IsOwnKalah(self, cell_index):
        assert cell_index >= 0 and cell_index < self.cells_number, 'Invalid cell index ' + str(cell_index)
        return self.active_player == 0 and cell_index == self.kalah0_index or self.active_player == 1 and cell_index == self.kalah1_index

    def MakeMove(self, move, log=False):
        if self.IsEnd:
            print('Game is over')
            return
        assert move >= 0 and move < self.cells_number and self.IsOwnCell(move) and \
               move != self.kalah0_index and move != self.kalah0_index and self.state[move] != 0, 'Impossible move ' + str(move)
        if log:
            print('Player', self.active_player, 'makes move:', move)
        self.history.SaveMove(MoveInfo(self.active_player, move, deepcopy(self.state)))

        # move chips
        chips_count = self.state[move]
        self.state[move] = 0
        cell_index = move
        while chips_count > 0:
            cell_index = (cell_index + 1) % self.cells_number
            if cell_index == self.kalah0_index and self.active_player == 1 or cell_index == self.kalah1_index and self.active_player == 0:
                continue
            self.state[cell_index] += 1
            chips_count -= 1

        # eat opponent chips
        if self.IsOwnCell(cell_index) and self.state[cell_index] == 1 and not self.IsOwnKalah(cell_index):
            self.AddToKalah(self.state[12 - cell_index] + 1)  # add chips from the opposite cell and 1 own chip from the current cell
            self.state[cell_index] = 0
            self.state[12-cell_index] = 0

        # change active player
        if not (self.active_player == 0 and cell_index == self.kalah0_index or self.active_player == 1 and cell_index == self.kalah1_index):
            self.active_player = (self.active_player + 1) % 2  # 0 -> 1 or 1 -> 0

        # check the end of game
        if self.IsGameOver():
            self.AddToKalah(self.GetRemainingChips())

            # clear cells except kalah
            start_index = 0 if self.active_player == 0 else 7
            for i in range(start_index, start_index + 6):
                self.state[i] = 0

            # find the winner
            if self.GetScore(0) > self.GetScore(1):
                self.winner = 0
            elif self.GetScore(0) < self.GetScore(1):
                self.winner = 1

            self.IsEnd = True
            if log:
                self.PrintResult()
        if log:
            self.PrintState()

    def UndoLastMove(self):
        self.state = deepcopy(self.history.GetLastState())
        self.active_player = self.history.GetLastActivePlayer()
        self.IsEnd = False
        self.winner = -1
        self.history.DeleteLastMove()

    def PrintResult(self):
        print("Game over!")
        print("Player 0: ", self.GetScore(0), ' scores')
        print("Player 1: ", self.GetScore(1), ' scores')
        if (self.winner != -1):
            print("Winner: Player", self.winner)
        else:
            print("Equal scores!")

    def MakeMoves(self, moves_array:list, log=False):
        for move in moves_array:
            self.MakeMove(move, log)

    def GetRemainingChips(self):
        if self.active_player == 0:
            return sum(self.state[0:6])
        else:
            return sum(self.state[7:13])

    def IsGameOver(self):
        isEnd = False
        if sum(self.state[0:self.kalah0_index]) == 0:
            self.active_player = 1
            isEnd = True
        elif sum(self.state[7:self.kalah1_index]) == 0:
            self.active_player = 0
            isEnd = True
        return isEnd

    def GetScore(self, player_id):
        assert player_id == 0 or player_id == 1, 'Incorrect player id'
        if player_id == 0:
            return self.state[self.kalah0_index]
        else:
            return self.state[self.kalah1_index]

    def AddToKalah(self, chips_number):
        if self.active_player == 0:
            self.state[self.kalah0_index] += chips_number
        else:
            self.state[self.kalah1_index] += chips_number
