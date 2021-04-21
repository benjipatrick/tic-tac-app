import Versus
from TicTacToe import TicTacToe
from Players import *

import numpy as np
import random

game = TicTacToe()

random_player = random_player(game).play
human_player = human_player(game).play
mcts_player = monte_carlo_player(game, iters=5000).play

versus = Versus.Versus(random_player, mcts_player, game)
print(versus.play_games(20))

