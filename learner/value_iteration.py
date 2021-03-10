import numpy as np
from learner.learner import Learner
from copy import deepcopy

class ValueIterationLearner(Learner):
    def __init__(self, env):
        super(ValueIterationLearner, self).__init__(env)
        self.name = "Value Iteration"

    def bellman_optimality_update(self, s, gamma, V):
        # these are not actually q values
        Q_values = []
        location = self.env._to_location(s)
        # following IA equation, reward is for R(s) not R(s_prime)
        reward = self.env.get_reward(location)
        for a in self.env.actions:
            q_value = 0
            for next_state, probability in self.env.transitions(s, a):
                # reward also pulled outside of probability
                q_value += probability * (gamma * V[next_state])
            Q_values.append(q_value)
        self.V[s] = reward + max(Q_values)

    def value_iteration(self, gamma, theta):
        # for keeping track in object
        self.gamma = gamma
        self.theta = theta
        i = 0
        while True:
            V_old = deepcopy(self.V)
            if i % 50 == 0:
                print('On iteration', i)
            delta = 0 # for stopping threshold theta
            for s in self.env.learnable_states:
                v = V_old[s]
                self.bellman_optimality_update(s, gamma, V_old)
                delta = max(delta, abs(v - self.V[s]))
            i += 1
            if delta < theta:
                print('Converged within theta margin at iteration', i)
                break
        for s in self.env.states:
            if s in self.env.learnable_states:
                self.q_greedify_policy(s, gamma)
            else:
                self.pi[s] = np.zeros(self.env.n_actions)