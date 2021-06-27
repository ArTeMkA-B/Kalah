from Kalah import *
from random import randint

player0 = 0
player1 = 0
equal_scores = 0
games_count = 10000
for i in range(games_count):
    kalah = Kalah()
    while not kalah.IsEnd:
        possible_moves = kalah.GetPossibleMoves()
        kalah.MakeMove(possible_moves[randint(0, len(possible_moves) - 1)])
    if kalah.winner == 0:
        player0 += 1
    elif kalah.winner == 1:
        player1 += 1
    else:
        equal_scores += 1

print('Simulation of', games_count, 'games:')
print('\tPlayer 0 wins:', player0, 'times (' + str(round(player0 / games_count * 100, 2)) + '%)')
print('\tPlayer 1 wins:', player1, 'times (' + str(round(player1 / games_count * 100, 2)) + '%)')
print('\tEqual scores:', equal_scores, 'times (' + str(round(equal_scores / games_count * 100, 2)) + '%)')