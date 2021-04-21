import numpy as np
import time
import Utils

class Versus():

    def __init__(self, player1, player2, game, show = False):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.show = show
    
    def play_game(self):
        players = [0, self.player1, self.player2]
        current_player = 1
        board = self.game.return_initial_board()
        turn = 0
        winner = self.game.get_game_status(board, turn)
        while winner == None:
            turn += 1

            if self.show:
                print('Turn, {0}, Player, {1}'.format(turn, current_player))
                print(self.game.get_board_representation(board))
            
            action = players[current_player](board, current_player, turn)
            valids = self.game.get_valid_actions(board)

            if self.show:
                print('Valid Moves: {}'.format(self.game.get_valid_actions(board)))
                print('Move Chosen: {}'.format(action))

            board = self.game.get_next_state(board, current_player, action)
            current_player = -current_player
            winner = self.game.get_game_status(board, turn)

        if self.show:
            print("Game Over. Result: {}".format(winner))
            print(self.game.get_board_representation(board))
        
        return winner

    def play_games(self, number_of_games):
        number_of_games //= 2
        player_one_wins = 0
        player_two_wins = 0
        draws = 0
        for _ in range(number_of_games):
            result = self.play_game()
            if result == 1: player_one_wins += 1
            elif result == -1: player_two_wins += 1
            else: draws += 1

        self.player1, self.player2 = self.player2, self.player1

        for _ in range(number_of_games):
            result = self.play_game()
            if result == -1: player_one_wins += 1
            elif result == 1: player_two_wins += 1
            else: draws += 1    
        
        return player_one_wins, player_two_wins, draws
