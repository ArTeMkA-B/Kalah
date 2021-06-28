from GoodBot import *
from simpleBot import *
from Kalah import *
from random import randint

player0 = 0
player1 = 0
equal_scores = 0
games_count = 1

counter = 0

# bot0 = GoodBot(0)
bot = SimpleBot(0)
showMoves = False

for i in range(games_count):
    kalah = Kalah()
    while not kalah.IsEnd:
        counter += 1
        possible_moves = kalah.GetPossibleMoves()
        if kalah.active_player == bot.id:
            chosen_move = bot.ChooseMove(kalah.state, possible_moves, kalah.GetKalahIndex(), kalah)
            kalah.MakeMove(chosen_move, showMoves)
            #chosen_move = bot.ChooseMove(kalah)
        else:
            kalah.MakeMove(possible_moves[randint(0, len(possible_moves) - 1)], showMoves)
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
print('\tNumber of moves in each game (mean): ', counter // games_count)
