
import random
import config as cfg
import numpy as np
import pickle


class QLearn:
    
    def __init__(self, actions, alpha=cfg.alpha, gamma=cfg.gamma, epsilon=cfg.epsilon, min_epsilon=cfg.min_epsilon, epsilon_decay=cfg.epsilon_decay):
        self.Q = {} # {(state, action): Q-value}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay
        self.actions = actions # a list of actions: [action0, action1, action2, ...]
    
    # Get the Q-value of an action in a certain state, default value is 0.0
    def getQ(self, state, action):
        return self.Q.get((state, action), 0.0)
    
    # When in a certain state, find the best action while exploring new grid by chance (epsilon-greedy strategy)
    def chooseAction(self, state):
        if random.random() < self.epsilon: # exploration
            action = random.choice(self.actions) # choose a random action
        else: # exploitation
            Q = [self.getQ(state, act) for act in self.actions] # Q-values for a specific state for all actions
            max_Q = max(Q)
            # In case there are several max Q-values, select one at random
            if Q.count(max_Q) > 1:
                best_actions = [self.actions[i] for i in range(len(self.actions)) if Q[i] == max_Q]
                action = random.choice(best_actions)
            else:
                action = self.actions[Q.index(max_Q)]
        return action
    
    # Learn
    def learnQ(self, state1, action, state2, reward):
        old_Q = self.Q.get((state1, action), None)
        if old_Q is None:
            self.Q[(state1, action)] = reward
        else:
            next_max_Q = max([self.getQ(state2, act) for act in self.actions])
            self.Q[(state1, action)] = old_Q + self.alpha * (reward + self.gamma * next_max_Q)
    
    # Exploration rate decay, applied after each episode
    def epsilonDecay(self, episode):
        self.epsilon = self.min_epsilon + (1 - self.min_epsilon) * np.exp(-self.epsilon_decay * episode)

    def saveAI(self, filename):
        with open(f'{filename}.pkl', 'wb') as handle:
            data = [self.Q, self.epsilon, self.epsilon_decay,
                    self.alpha, self.gamma, self.min_epsilon, self.actions]
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
    def loadAI(self, filename):
        with open(f'{filename}.pkl', 'rb') as handle:
            data = pickle.load(handle)
            self.Q = data[0]
            self.epsilon = data[1]
            self.epsilon_decay = data[2]
            self.alpha = data[3]
            self.gamma = data[4]
            self.min_epsilon = data[5]
            self.actions = data[6]