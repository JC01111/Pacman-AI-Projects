# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Feature: Get the distance from pac to foods
        dist_to_foods = [util.manhattanDistance(newPos, food) for food in newFood.asList()]
        nearestFood = min(dist_to_foods) if dist_to_foods else 0
        foodVal = 1.0 / (nearestFood + 1)
        # Feature: The distance from pac to ghost
        ghostVals = []
        for ghostState in newGhostStates:
            dist_to_ghost = util.manhattanDistance(newPos, ghostState.getPosition())
            if ghostState.scaredTimer > 0:
                ghostVal = 1.0 / (dist_to_ghost + 1)
            else:
                ghostVal = -1.0 / (dist_to_ghost + 1)
            ghostVals.append(ghostVal)

        return successorGameState.getScore() + 2 * foodVal + 3 * sum(ghostVals)

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # Initialize the value() and return the best_action
        # Follow the structure from notes06 p5
        value, best_action = self.value(gameState, 0, 0)
        return best_action

    def value(self, gameState, depth, agentIndex):
        # Base case
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex == 0:
            return self.max_value(gameState, depth)
        else:
            return self.min_value(gameState, depth, agentIndex)

    def max_value(self, gameState, depth):
        v = float("-inf")
        best_action = Directions.STOP # Default to be stop
        for action in gameState.getLegalActions(0):
            successor_value, _ = self.value(gameState.generateSuccessor(0, action), depth, 1)
            if successor_value > v:
                v = successor_value
                best_action = action
        return v, best_action

    def min_value(self, gameState, depth, agentIndex):
        v = float("inf")
        best_action = Directions.STOP
        for action in gameState.getLegalActions(agentIndex):
            # Case when this is the last ghost
            if agentIndex == gameState.getNumAgents() - 1:
                successor_value, _ = self.value(gameState.generateSuccessor(agentIndex, action), depth + 1, 0)
            else:
                successor_value, _ = self.value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
            if successor_value < v:
                v = successor_value
                best_action = action
        return v, best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Initialize
        alpha = float('-inf')
        beta = float('inf')
        _, best_action = self.max_value(gameState, 0, alpha, beta)
        return best_action

    def value(self, gameState, depth, agentIndex, alpha, beta):
        # Base case
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex == 0:
            return self.max_value(gameState, depth, alpha, beta)
        else:
            return self.min_value(gameState, depth, agentIndex, alpha, beta)

    def max_value(self, gameState, depth, alpha, beta):
        v = float('-inf')
        best_action = Directions.STOP
        for action in gameState.getLegalActions(0):
            successor_value, _ = self.value(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)
            if successor_value > v:
                v = successor_value
                best_action = action
            # Due to pruning, early return
            if v > beta:
                return v, best_action
            alpha = max(alpha, v)
        return v, best_action

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        v = float('inf')
        best_action = Directions.STOP
        for action in gameState.getLegalActions(agentIndex):
            # Check if this is the last ghost
            if agentIndex == gameState.getNumAgents() - 1:
                successor_value, _ = self.value(gameState.generateSuccessor(agentIndex, action), depth + 1, 0, alpha, beta)
            else:
                successor_value, _ = self.value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1, alpha, beta)
            if successor_value < v:
                v = successor_value
                best_action = action
            # Due to pruning, early return
            if v < alpha:
                return v, best_action
            beta = min(beta, v)
        return v, best_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        _, best_action = self.value(gameState, 0, 0)
        return best_action

    def value(self, gameState, depth, agentIndex):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex == 0:
            return self.max_value(gameState, depth)
        else:
            return self.exp_value(gameState, depth, agentIndex)

    def max_value(self, gameState, depth):
        v = float('-inf')
        best_action = Directions.STOP
        for action in gameState.getLegalActions(0):
            successor_value, _ = self.value(gameState.generateSuccessor(0, action), depth, 1)
            if successor_value > v:
                v = successor_value
                best_action = action
        return v, best_action

    def exp_value(self, gameState, depth, agentIndex):
        v = 0
        best_action = Directions.STOP
        numAgents = gameState.getNumAgents()
        legalActions = gameState.getLegalActions(agentIndex)
        p = 1 / len(legalActions) # Probability
        expectedMax_and_action = []

        for action in legalActions:
            # Check if the last ghost
            if agentIndex == numAgents - 1:
                successor_value, _ = self.value(gameState.generateSuccessor(agentIndex, action), depth + 1, 0)
            else:
                successor_value, action = self.value(gameState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
            # Append the value and action to the list
            expectedMax_and_action.append((successor_value, action))
            v += p * successor_value
        # Find the max value of the ghosts', then use that action
        best_action = max(expectedMax_and_action, key=lambda x: x[0])[1]
        return v, best_action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    - distance to foods
    - distance to ghosts
    - distance to capsules
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    newCapsules = currentGameState.getCapsules()
    newGhostStates = currentGameState.getGhostStates()

    # First feature: Position the the Foods
    dist_to_foods = [util.manhattanDistance(newPos, food) for food in newFood]
    nearestFood = min(dist_to_foods) if dist_to_foods else 0
    foodVal = 1.0 / (nearestFood + 1)

    # Second featue: Position to the ghosts
    ghostVals = []
    for ghostState in newGhostStates:
        dist_to_ghost = util.manhattanDistance(newPos, ghostState.getPosition())
        if ghostState.scaredTimer > 0:
            # Encourage the pacman to eat ghosts by adding timer as value
            ghostVal = (1.0 / (dist_to_ghost + 1)) + 2 * ghostState.scaredTimer
        else:
            ghostVal = -1.0 / (dist_to_ghost + 1)
        ghostVals.append(ghostVal)

    # Third feature: newPos to the capsules
    dist_to_capsules = [util.manhattanDistance(newPos, capsule) for capsule in newCapsules]
    nearestCapsule = min(dist_to_capsules) if dist_to_capsules else 0
    capsuleVal = 1.0 / (nearestCapsule + 1)

    return currentGameState.getScore() + 2 * foodVal + 2 * capsuleVal + 3 * sum(ghostVals)

# Abbreviation
better = betterEvaluationFunction
