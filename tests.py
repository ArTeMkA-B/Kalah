from main import *

kalah = Kalah()
assert kalah.state == [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0], kalah.state
assert kalah.GetScore(0) == 0
assert kalah.GetScore(1) == 0
kalah.MakeMove(1)
assert kalah.state == [6, 0, 7, 7, 7, 7, 1, 7, 6, 6, 6, 6, 6, 0], kalah.state
kalah.MakeMove(9)
assert kalah.state == [7, 1, 7, 7, 7, 7, 1, 7, 6, 0, 7, 7, 7, 1], kalah.state
kalah.MakeMove(5)
assert kalah.state == [7, 1, 7, 7, 7, 0, 2, 8, 7, 1, 8, 8, 8, 1], kalah.state
kalah.MakeMove(12)
assert kalah.state == [8, 2, 8, 8, 8, 1, 2, 9, 7, 1, 8, 8, 0, 2], kalah.state
kalah.MakeMove(1)
assert kalah.state == [8, 0, 9, 9, 8, 1, 2, 9, 7, 1, 8, 8, 0, 2], kalah.state
kalah.MakeMove(11)
assert kalah.state == [9, 1, 10, 10, 9, 2, 2, 9, 7, 1, 8, 0, 1, 3], kalah.state
kalah.MakeMove(3)
assert kalah.state == [10, 1, 10, 0, 10, 3, 3, 10, 8, 2, 9, 1, 2, 3], kalah.state
kalah.MakeMove(9)
assert kalah.state == [10, 1, 10, 0, 10, 3, 3, 10, 8, 0, 10, 2, 2, 3], kalah.state
kalah.MakeMove(1)
assert kalah.state == [10, 0, 11, 0, 10, 3, 3, 10, 8, 0, 10, 2, 2, 3], kalah.state
kalah.MakeMove(11)
assert kalah.state == [10, 0, 11, 0, 10, 3, 3, 10, 8, 0, 10, 0, 3, 4], kalah.state
kalah.MakeMove(12)
assert kalah.state == [11, 1, 11, 0, 10, 3, 3, 10, 8, 0, 10, 0, 0, 5], kalah.state
kalah.MakeMoves([0, 8, 1, 12, 11, 12, 9, 3])
assert kalah.state == [1, 0, 14, 0, 13, 5, 5, 11, 0, 0, 13, 0, 0, 10], kalah.state
kalah.MakeMoves([5, 9, 4])
assert kalah.state == [2, 1, 15, 1, 0, 1, 10, 13, 0, 1, 16, 1, 1, 10], kalah.state
kalah.MakeMoves([12, 11, 5, 3, 7, 3, 12, 11, 1, 8, 4, 5, 2, 4, 2, 12, 11, 1, 9, 3, 4, 8])
assert kalah.state == [0, 0, 0, 0, 0, 5, 40, 1, 0, 0, 0, 0, 0, 26], kalah.state
kalah.MakeMove(5)
assert kalah.state == [0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 31], kalah.state
assert kalah.GetScore(0) == 41
assert kalah.GetScore(1) == 31
