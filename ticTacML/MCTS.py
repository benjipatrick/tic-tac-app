import math
import numpy as np
import Utils
import random
EPS = 1e-8

class MCTS():

    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.args = args
        self.Qsa = {} # stores the Q values for state and action
        self.Nsa = {} # stores the action visit count
        self.Ns = {} # stores the visit count
        self.Ps = {} # stores the policy returned by the neural network

        self.Es = {} # stores if the game has ended for board state
        self.Vs = {} # stores valid moves for board state
    
    def get_action_prob(self, board, player, temp=1, turn=1, show=False):
        for i in range(self.args.num_mcts_sims):
            self.search(board, player, turn)
        
        s = (board*player).tostring()
        counts = [self.Nsa[(s,a)] if (s,a) in self.Nsa else 0 for a in range(self.game.ACTION_SIZE)]

        if show:
            valids = self.game.get_valid_actions(board)
            p, v = self.nnet.predict(self.game.get_nnet_input_form(board, player))
            print(p*valids, v, player)

        if temp==0:
            
            best_action = np.argmax(counts)
            probs = [0]*len(counts)
            if counts == probs:
                valids = self.game.get_valid_actions(board)
                best_action = random.choice(valids)
            probs[best_action] = 1
            return probs
        
        counts = [x**(1./temp) for x in counts]
        probs = [x/float(sum(counts)) for x in counts]
        return probs
    
    def search(self, board, player, turn=1):
        s = (board*player).tostring()

        if turn>9:
            return -self.nnet.predict(self.game.get_nnet_input_form(board, player))[1]

        if s not in self.Es:
            self.Es[s] = self.game.get_game_status(turn)
           
        if self.Es[s] != None: 
            return -self.Es[s]
        
        if s not in self.Ps:
            # leaf node
            self.Ps[s], v = self.nnet.predict(self.game.get_nnet_input_form(board, player))
            valids = self.game.get_valid_actions(board)
            self.Ps[s] = self.Ps[s] * valids # masks invalid moves
            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s # renormalize
            else:
                # if all valid moves were masked
                print("All valid moves masked")
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])
            
            self.Vs[s] = valids
            self.Ns[s] = 0
            return -v
        
        valids = self.Vs[s]
        cur_best = -float('inf')
        best_action = -1

        # pick the action with the highest upper confidence bound
        for a in range(self.game.ACTION_SIZE):
            if valids[a]:
                if (s,a) in self.Qsa:
                    u = self.Qsa[(s,a)] + self.args.cpuct*self.Ps[s][a]*math.sqrt(self.Ns[s])/(1+self.Nsa[(s,a)])
                else:
                    u = self.args.cpuct*self.Ps[s][a]*math.sqrt(self.Ns[s] + EPS)  

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        next_s = self.game.get_next_state(board, player, a)

        v = self.search(next_s, -player, turn+1)

        if (s,a) in self.Qsa:
            self.Qsa[(s,a)] = (self.Nsa[(s,a)]*self.Qsa[(s,a)] + v)/(self.Nsa[(s,a)]+1)
            self.Nsa[(s,a)] += 1

        else:
            self.Qsa[(s,a)] = v
            self.Nsa[(s,a)] = 1

        self.Ns[s] += 1
        return -v