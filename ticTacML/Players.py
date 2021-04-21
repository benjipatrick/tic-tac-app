import numpy as np
import Utils
import copy
import random
import time

from PURE_MCTS import PURE_MCTS 

class random_player():
    def __init__(self, game):
        self.game = game
    
    def play(self, board, player=None, turn=None):
        return random.choice(self.game.get_valid_actions(board))

class human_player():
    def __init__(self, game):
        self.game = game

    def play(self, board, player=None, turn=None):
        legal_actions = self.game.get_valid_actions(board)
        print(legal_actions)
        choice = -1
        while choice not in legal_actions:
            try:
                choice = int(input("Enter choice:"))
            except ValueError:
                pass
        return choice

class monte_carlo_player():
    def __init__(self, game, iters=100, show=False):
        self.game = game     
        self.mcts = None
        self.turns = 0
        self.iters = iters
        self.show = show
        
    
    def play(self, board, player, turn=1):
        if not self.mcts:
            self.mcts = PURE_MCTS(self.game, player, self.show)  
        action = self.mcts.find_next_action(board, player, turn, max_iters=self.iters)
        return action