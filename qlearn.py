
import random
import config as cfg
import numpy as np


class QLearn:
    
    def __init__(self, actions, alpha=cfg.alpha, gamma=cfg.gamma, epsilon=cfg.epsilon, min_epsilon=cfg.min_epsilon, epsilon_decay=cfg.epsilon_decay):
        self.Q = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay
        self.actions = actions # a list of actions
    
    # Get the Q-value of an action in a certain state, default value is 0.0
    def getQ(self, state, action):
        return self.Q.get((state, action), 0.0)
    
    # When in a certain state, find the best action while exploring new grid by chance (epsilon-greedy strategy)
    def chooseAction(self, state):
        if random.random() < self.epsilon: # exploration
            action = random.choice(self.actions) # choose a random action
        else: # exploitation
            Q = [self.getQ(state, act) for act in self.actions] # Q-values for a specific state for all actions
            maxQ = max(Q)
            # In case there are several max Q-values, select one at random
            if Q.count(maxQ) > 1:
                bestActions = [self.actions[i] for i in range(len(self.actions)) if Q[i] == maxQ]
                action = random.choice(bestActions)
            else:
                action = self.actions[Q.index(maxQ)]
        return action
    
    # Learn
    def learnQ(self, state1, action, state2, reward):
        oldQ = self.Q.get((state1, action), None)
        if oldQ is None:
            self.Q[(state1, action)] = reward
        # update Q-value
        else:
            next_maxQ = max([self.getQ(state2, act) for act in self.actions])
            self.Q[(state1, action)] = (1 - self.alpha) * oldQ + self.alpha * (reward + self.gamma * next_maxQ)
    
    # Exploration rate decay
    def epsilonDecay(self, episode):
        self.epsilon = self.min_epsilon + (1 - self.min_epsilon) * np.exp(-self.epsilon_decay * episode)

