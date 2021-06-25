class Kalah:
    def __init__(self):
        self.state = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
        self.cells_number = 14
        self.active_player = 0  # players: 0 and 1
        self.kalah1_index = 6
        self.kalah2_index = 13
        self.IsEnd = False

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
        return self.active_player == 0 and cell_index == self.kalah1_index or self.active_player == 1 and cell_index == self.kalah2_index

    def MakeMove(self, move, log=False):

        if self.IsEnd:
            print('Game is over')
            return
        assert move >= 0 and move < self.cells_number and self.IsOwnCell(move) and \
               move != self.kalah1_index and move != self.kalah2_index and self.state[move] != 0, 'Impossible move ' + str(move)

        if log:
            print('Player', self.active_player, 'makes move:', move)

        # move chips
        chips_count = self.state[move]
        self.state[move] = 0
        cell_index = move
        while chips_count > 0:
            cell_index = (cell_index + 1) % self.cells_number
            if cell_index == 6 and move >= 7 or cell_index == 13 and move <= 5:
                continue
            self.state[cell_index] += 1
            chips_count -= 1

        # eat opponent chips
        if self.IsOwnCell(cell_index) and self.state[cell_index] == 1 and not self.IsOwnKalah(cell_index):
            self.AddToKalah(self.state[12 - cell_index] + 1)  # chips from the opposite cell and 1 own chip from current cell
            self.state[cell_index] = 0
            self.state[12-cell_index] = 0

        # change active player
        if not (self.active_player == 0 and cell_index == self.kalah1_index or self.active_player == 1 and cell_index == self.kalah2_index):
            self.active_player = (self.active_player + 1) % 2

        # check the end of game
        if self.IsGameOver():
            self.AddToKalah(self.GetRemainingChips())
            if self.active_player == 0:
                for i in range(0, 6):
                    self.state[i] = 0
            else:
                for i in range(7, 13):
                    self.state[i] = 0
            self.PrintResult()
            self.IsEnd = True

    def PrintResult(self):
        if self.GetScore(0) > self.GetScore(1):
            winner = 0
        elif self.GetScore(0) < self.GetScore(1):
            winner = 1
        else:
            winner = -1
        print("Game over!")
        print("Player 0: ", self.GetScore(0), ' scores')
        print("Player 1: ", self.GetScore(1), ' scores')
        if (winner != -1):
            print("Winner: Player", winner)
        else:
            print("Equal scores!")

    def MakeMoves(self, moves_array):
        for move in moves_array:
            self.MakeMove(move)

    def GetRemainingChips(self):
        if self.active_player == 0:
            return sum(self.state[0:6])
        else:
            return sum(self.state[7:13])

    def IsGameOver(self):
        return self.active_player == 0 and sum(self.state[7:13]) == 0 or self.active_player == 1 and sum(self.state[0:6]) == 0

    def GetScore(self, player_id):
        assert player_id == 0 or player_id == 1, 'Incorrect player id'
        if player_id == 0:
            return self.state[self.kalah1_index]
        else:
            return self.state[self.kalah2_index]

    def AddToKalah(self, chips_number):
        if self.active_player == 0:
            self.state[self.kalah1_index] += chips_number
        else:
            self.state[self.kalah2_index] += chips_number