import math
import numpy as np
import Utils
import random
import sys
EPS = 1e-8

class State():
    def __init__(self, board, turns, player, action_to_state, visit_count=0, win_score=0):
        self.board = board
        self.player = player
        self.opponent = -player
        self.visit_count = visit_count
        self.win_score = win_score
        self.action_to_state = action_to_state
        self.turns = turns
    
    def get_next_states(self, game):
        for action in game.get_valid_actions(self.board):
            next_board = game.get_next_state(self.board, self.player, action)
            yield State(next_board, self.turns+1, -self.player, action)
    
    def random_play(self, game):
        legal_actions = game.get_valid_actions(self.board)
        if len(legal_actions) == 0:
            return
        action = random.choice(legal_actions)
        next_board = game.get_next_state(self.board, self.player, action)
        return State(next_board, self.turns+1, -self.player, action)

def uct_value(total_visit, node_win_score, node_visit):
    if node_visit == 0: return -sys.maxsize
    return (node_win_score / node_visit) + ((1/math.sqrt(2)) * math.sqrt(math.log(total_visit)/node_visit))

def find_best_node(node):
    parent_visit = node.state.visit_count
    best_node = None
    for c in node.children:
        if best_node is None:
            best_node = (c, uct_value(parent_visit, c.state.win_score, c.state.visit_count))
        else:
            val = uct_value(parent_visit, c.state.win_score, c.state.visit_count)
            if val > best_node[1]:
                best_node = (c, val)
    return best_node[0]

class Node():
    def __init__(self, state, parent=None, children=[]):
            self.state = state
            self.parent = parent
            self.children = children

    def max_scoring_child(self):
        best_nodes = []
        best_score = 0
        for c in self.children:
            if len(best_nodes) == 0:
                best_nodes += [c]
                best_score = c.state.win_score
            else:
                val = c.state.win_score
                if val > best_score:
                    best_nodes = [c]
                    best_score = val
                elif val == best_score:
                    best_nodes += [c]
        return random.choice(best_nodes)

    def most_visited_child(self):
        best_nodes = []
        best_score = 0
        for c in self.children:
            if len(best_nodes) == 0:
                best_nodes = [c]
                best_score = c.state.visit_count
            else:
                val = c.state.visit_count
                if val > best_score:
                    best_nodes = [c]
                    best_score = val
                elif val == best_score:
                    best_nodes += [c]
        # get max scoring if multiple nodes have the same visit count
        top_scoring_nodes = []
        best_score = 0
        for c in best_nodes:
            if len(top_scoring_nodes) == 0:
                top_scoring_nodes += [c]
                best_score = c.state.win_score
            else:
                val = c.state.win_score
                if val > best_score:
                    top_scoring_nodes = [c]
                    best_score = val
                elif val == best_score:
                    top_scoring_nodes += [c]
        return random.choice(top_scoring_nodes)

class Tree():
    def __init__(self, root = Node(State([[]], 0, 0, None), None, [])):
        self.root = root


class PURE_MCTS():

    def __init__(self, game, player, show=False):
        self.WIN_SCORE = 1
        self.LOSE_SCORE = -1
        self.DRAW_SCORE = 0
        self.player = player
        self.opponent = -player
        self.tree = None
        self.game = game
        self.show = show
    
    def find_next_action(self, board, player, turns, max_iters=1000):
        found = False
        if not found:
            self.tree = Tree()
            self.tree.root.state.board = board
            self.tree.root.children = []
            self.tree.root.state.turns = turns
            self.tree.root.state.player = player
            
        if len(self.tree.root.children) == 0:
            self.expand_node(self.tree.root)

        iterations = 0

        while (iterations < max_iters) and len(self.tree.root.children) != 1:
            # selection
            promising_node = self.select_promising_node(self.tree.root)
            # expansion
            if not self.game.get_game_status(promising_node.state.board, promising_node.state.turns):
                self.expand_node(promising_node)
            self.simulate_and_back_propagate(promising_node, player)
            
            iterations += 1

        winner_node = self.tree.root.most_visited_child()
        action = winner_node.state.action_to_state
        if(self.show):
            for node in self.tree.root.children:
                print("Move %s had a score of %s and a visit count of %s" % (node.state.action_to_state, node.state.win_score, node.state.visit_count))
            print("%s rollouts performed!" % (iterations))
            print("Winner node had a score of: %s, and a visit count of: %s"  % (winner_node.state.win_score, winner_node.state.visit_count))

        self.tree.root = winner_node
        return winner_node.state.action_to_state

    @staticmethod
    def select_promising_node(root_node):  
        node = root_node
        while len(node.children) != 0:
            node = find_best_node(node)
        return node
    
    def expand_node(self, node):
        for state in node.state.get_next_states(self.game):
            new_node = Node(state, node, [])
            new_node.state.player = -(node.state.player)
            node.children += [new_node]
            
    def back_propagate(self, node_to_explore, player):
        temp_node = node_to_explore
        while temp_node != None:
            temp_node.state.visit_count += 1
            if temp_node.state.player == -player:
                temp_node.state.win_score += self.WIN_SCORE
            elif temp_node.state.player != player:
                temp_node.state.win_score += self.LOSE_SCORE
            temp_node = temp_node.parent
    
   
    def simulate_random_playout(self, node):
        temp_node = node
        temp_state = temp_node.state

        board_status = self.game.get_game_status(temp_state.board, temp_state.turns)

        if board_status == self.player:
            temp_node.parent.state.win_score = self.LOSE_SCORE
            return board_status
        while board_status == None:
            temp_state = temp_state.random_play(self.game)
            board_status = self.game.get_game_status(temp_state.board, temp_state.turns)
            
        # print("time in %s" % (time.time() - startt))
        return board_status

    def simulate_and_back_propagate(self, promising_node, player):
        # simulation
        
        if len(promising_node.children) > 0:
            promising_node = random.choice(promising_node.children)
        playout_result = self.simulate_random_playout(promising_node)
        # update
        self.back_propagate(promising_node, playout_result)  