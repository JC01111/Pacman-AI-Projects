# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            prev_values = self.values.copy()
            for state in self.mdp.getStates():
                max_val = float('-inf')
                # When a state has no available action (terminal), we skip it
                for action in self.mdp.getPossibleActions(state):
                    q_val = self.computeQValueFromValues(state, action)
                    max_val = max(max_val, q_val)
                    # Updating each state value in self.values
                    prev_values[state] = max_val
            self.values = prev_values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_val = 0
        for nextState, T in self.mdp.getTransitionStatesAndProbs(state, action):
            q_val += T * (self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState])
        return q_val


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        action_vals = self.mdp.getPossibleActions(state)
        if len(action_vals) == 0:
            return None
        return max((self.computeQValueFromValues(state, action), action) for action in action_vals)[1]


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        pq = util.PriorityQueue()
        predecessors = {}
        # Compute the predecessors of all states
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                for action in self.mdp.getPossibleActions(state):
                    for nextState, P in self.mdp.getTransitionStatesAndProbs(state, action):
                        if P > 0:
                            if nextState not in predecessors:
                                predecessors[nextState] = set()
                            predecessors[nextState].add(state)
        # Prioritize the state
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                diff = abs(self.values[state] - max([self.computeQValueFromValues(state, action)
                 for action in self.mdp.getPossibleActions(state)]))
                pq.push(state, -diff)

        # Iterations
        for i in range(self.iterations):
            if pq.isEmpty():
                break
            currState = pq.pop()
            if not self.mdp.isTerminal(currState):
                # Update currState to Q_max
                self.values[currState] = max([self.computeQValueFromValues(currState, action) for action in self.mdp.getPossibleActions(currState)])
            # Update the currState's predecessor
            for predecessor in predecessors[currState]:
                diff = abs(self.values[predecessor] - max([self.computeQValueFromValues(predecessor, action) for action in self.mdp.getPossibleActions(predecessor)]))
                if diff > self.theta:
                    pq.update(predecessor, -diff)
