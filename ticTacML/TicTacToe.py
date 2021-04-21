import sys
import numpy as np
import math
# import Utils

class TicTacToe():
    WIN_CONDITIONS = [
        [0,1,2],
        [0,3,6],
        [0,4,8],
        [1,4,7],
        [2,4,6],
        [2,5,8],
        [3,4,5],
        [6,7,8]
    ]

    ACTION_SIZE = 9
    
    def return_initial_board(self):
        return np.array([None]*9)
    
    def get_next_state(self, board, player, action):
        # print(action)
        b = np.copy(board)
        b[action] = player
        return b
    
    def get_valid_actions(self, board):
        valid_moves = []
        for i, m in enumerate(board):
            if m == None:
                valid_moves += [i]
        return valid_moves

    '''
    Returns 0 if game in progress, -1/1 if a player has won, None if the game is drawn
    '''
    def get_game_status(self, board, turn):
        # Check if either player has won
        for condition in self.WIN_CONDITIONS:
            x, y, z = [board[c] for c in condition]
            if (x == y == z == 1) or (x == y == z == -1):
                return x
                
        # Check if game is drawn
        if turn+1 > self.ACTION_SIZE: return 0
        
    
    def get_board_representation(self, board):
        temp_board = []
        for i, n in enumerate(board):
            if n == 1: temp_board += ['X']
            elif n == -1: temp_board += ['O']
            else: temp_board += ['_']
        return '{0} {1} {2}\n{3} {4} {5}\n{6} {7} {8}\n'.format(*temp_board)

    