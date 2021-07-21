from GoodBot import *
from SimpleBot import *
from RandomBot import *
from Kalah import *
from time import time

player0_win = 0
player1_win = 0
equal_scores = 0
games_count = 5000
counter = 0

log = False
player0 = RandomBot(0, log=log)
player1 = GoodBot(1, log=log)
showMoves = False

start_time = time()
for i in range(games_count):
    if log:
        print("Game", i + 1, "--------------------------------")
    kalah = Kalah()
    while not kalah.IsEnd:
        if kalah.active_player == player0.id:
            chosen_moves = player0.ChooseMove(kalah)
        else:
            chosen_moves = player1.ChooseMove(kalah)
        kalah.MakeMoves(chosen_moves, showMoves)
        counter += len(chosen_moves)
    if log:
        print('     ', kalah.state)
    if kalah.winner == 0:
        player0_win += 1
    elif kalah.winner == 1:
        player1_win += 1
        if log:
            print('\n' * 50)
    else:
        equal_scores += 1
end_time = time()

print('Simulation of', games_count, 'games:')
print('\tPlayer 0 wins:', player0_win, 'times (' + str(round(player0_win / games_count * 100, 2)) + '%)')
print('\tPlayer 1 wins:', player1_win, 'times (' + str(round(player1_win / games_count * 100, 2)) + '%)')
print('\tEqual scores:', equal_scores, 'times (' + str(round(equal_scores / games_count * 100, 2)) + '%)')
print('\tMean number of moves in each game:', counter // games_count)
print("Simulation time:", str(round(end_time - start_time, 3)) + 's')
