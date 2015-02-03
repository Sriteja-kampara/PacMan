# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        # print "legalMoves: %s, scores: %s, bestScore: %f , bestIndices: %s, chosenIndex: %d" % (legalMoves, scores, bestScore, bestIndices, chosenIndex)
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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

        # Initialize minimum distance to Ghosts
        # Find the minimum distance of Ghost which threats Pacman the most.
        minDistToGhost = 99999999
        for ghostState in newGhostStates:
            distGhost = manhattanDistance(newPos, ghostState.getPosition())
            if distGhost < minDistToGhost:
                minDistToGhost = distGhost

        # Initialize minimum distance to Foods
        # Find the minimum distance of Food which Pacman eat nearby.
        curFood = currentGameState.getFood()
        minDistToFood = 99999999
        for foodPosition in curFood.asList():
            distFood = manhattanDistance(newPos, foodPosition)
            if distFood < minDistToFood:
                minDistToFood = distFood

        # Consider three parameters to get the adjusted evaluation
        # (1) number of food left, (2) closeness of the food and (3) minimal distance to a ghost.
        # with each priorities are 40%, 30%, and 30% respectively

        adjustedEvaluation = - (len(newFood.asList()) * 0.4 + minDistToFood * 0.3 + (max(successorGameState.getWalls().width, successorGameState.getWalls().height) - minDistToGhost) * 0.3)
        return adjustedEvaluation

def scoreEvaluationFunction(currentGameState):
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
    # We used this global variable to compare with the number of recurssive calls of AlphaBetaAgent
    # callsCount = 0

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"

        # MinimaxAgent.callsCount = 0

        # If the game state is lost or win then just return the evaluation value
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        # Calling maxValue with game state, depth, number of agents and the agent index
        # This leads recursion calls in MiniMax tree to make a decision
        finalDirection = self.maxValue(gameState, self.depth * gameState.getNumAgents(), gameState.getNumAgents(), 0)
        # print("Number of Calls: ", MinimaxAgent.callsCount)
        return finalDirection[1]

    # The helper function to remove STOP action to improve efficiency
    def removeStop(self, legalMoves):
        stopDirection = Directions.STOP
        if stopDirection in legalMoves:
            legalMoves.remove(stopDirection)

    # The maxValue method for PacMan whose agent index is zero
    # Note that the initial depth is self.depth * gameState.getNumAgents()
    # because we considered the "level" of depth to be a Max and Min recursion calls
    def maxValue(self, gameState, depth, numOfAgents, agentIndex):
        # MinimaxAgent.callsCount += 1

        # Get the legal moves list and remove stops to improve the efficiency
        legalMoves = gameState.getLegalActions(agentIndex)
        self.removeStop(legalMoves)

        # The next states, either passed in to getAction or generated via GameState.generateSuccessor
        nextStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
        if depth == 0 or len(nextStates) == 0:
            return (self.evaluationFunction(gameState), Directions.STOP)

        maxValue = -9999999
        action = legalMoves[0]
        moveIndex = 0
        chooseMax = []

        # There are only one case to call minValue from Pacman perspective
        for nextState in nextStates:
            res = self.minValue(nextState, depth-1, numOfAgents-2, numOfAgents, (agentIndex+1)%numOfAgents)
            chooseMax.append(res)
            if res > maxValue:
                maxValue = res
                action = legalMoves[moveIndex]
            moveIndex = moveIndex + 1

        return (maxValue, action)

    # The minValue method for each ghost whose index is agentIndex
    def minValue(self, gameState, depth, numOfMins, numOfAgents, agentIndex):
        # MinimaxAgent.callsCount += 1

        # Get the legal moves list and remove stops to improve the efficiency
        legalMoves = gameState.getLegalActions(agentIndex)
        self.removeStop(legalMoves)

        # The next states, either passed in to getAction or generated via GameState.generateSuccessor
        nextStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
        chooseMin = []

        # Considering three cases:
        # 1. If there is no more depth or next states then return evaluation value
        if depth == 0 or len(nextStates) == 0:
            return self.evaluationFunction(gameState)

        # 2. If all ghosts are evaluated then call maxValue for Pacman agent
        if numOfMins == 0:
            for nextState in nextStates :
                res =  self.maxValue(nextState, depth-1,  numOfAgents, (agentIndex+1)%numOfAgents)
                chooseMin.append(res[0])

        #3. If there are more ghosts left then call minValue for Ghost agent
        else:
            for nextState in nextStates:
                res = self.minValue(nextState, depth-1, numOfMins-1, numOfAgents, (agentIndex+1)%numOfAgents)
                chooseMin.append(res)

        # Return the minimum value each time
        return min(chooseMin)



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    # We used this global variable to compare with the number of recurssive calls of MinimaxAgent
    # callsCount = 0

    def getAction(self, gameState):

        """
          Returns the minimax action using self.depth and self.evaluationFunction
       """
        "*** YOUR CODE HERE ***"

        # AlphaBetaAgent.callsCount = 0
        # If the game state is lost or win then just return the evaluation value
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        # This part is almost the same with MinimaxAgent other than two additional parameters of alpha and beta values
        # by recursion calls in MiniMax tree to make a decision
        # alpha = the best choice of the highest values we have found so far along the path for MAX.
        #         (initializes -9999999)
        # beta = the best choice of the lowest values we have found so far along the path for MIN.
        #         (initializes +9999999)

        finalDirection = self.maxValueAlphaBeta(gameState, self.depth * gameState.getNumAgents(), gameState.getNumAgents(), 0, -9999999, 9999999)
        # print("Number of Calls: ", AlphaBetaAgent.callsCount)
        return finalDirection[1]

    # The helper function to remove STOP action to improve efficiency
    def removeStop(self, legalMoves):
        stopDirection = Directions.STOP
        if stopDirection in legalMoves:
            legalMoves.remove(stopDirection)

    # The maxValue method for PacMan whose agent index is zero
    def maxValueAlphaBeta(self, gameState, depth, numOfAgents, agentIndex, alpha, beta):
        # AlphaBetaAgent.callsCount += 1
        legalMoves = gameState.getLegalActions(agentIndex)
        self.removeStop(legalMoves)

        # The next states, either passed in to getAction or generated via GameState.generateSuccessor
        nextStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
        if depth == 0 or len(nextStates) == 0:
            return (self.evaluationFunction(gameState), Directions.STOP)

        maxValue = -9999999
        action = legalMoves[0]
        moveIndex = 0
        chooseMax = []

        # There are only one case to call minValue from Pacman perspective
        for nextState in nextStates:
            res = self.minValueAlphaBeta(nextState, depth-1, numOfAgents-2, numOfAgents, (agentIndex+1)%numOfAgents, alpha, beta)
            chooseMax.append(res)
            if res > maxValue:
                maxValue = res
                action = legalMoves[moveIndex]
                # Check "cut-off" condition
                if res > alpha: # If alpha is smaller than the current Max value
                    alpha = res # Then replace alpha with the current Max value
                if alpha >= beta: # When alpha value is larger than beta value
                    return (alpha, action)  # beta cut-off
            moveIndex = moveIndex + 1

        return (maxValue, action)

    # The minValue method for each ghost whose index is agentIndex
    def minValueAlphaBeta(self, gameState, depth, numOfMins, numOfAgents, agentIndex, alpha, beta):
        # AlphaBetaAgent.callsCount += 1

        legalMoves = gameState.getLegalActions(agentIndex)
        self.removeStop(legalMoves)

        # The next states, either passed in to getAction or generated via GameState.generateSuccessor
        nextStates = [gameState.generateSuccessor(agentIndex, action) for action in legalMoves]
        chooseMin = []

        # Considering three cases:
        # Case 1. If there is no more depth or next states then return evaluation value
        if depth == 0 or len(nextStates) == 0:
            return self.evaluationFunction(gameState)

        # Case 2. If all ghosts are evaluated then call maxValue for Pacman agent
        if numOfMins == 0:
            for nextState in nextStates:
                res =  self.maxValueAlphaBeta(nextState, depth-1,  numOfAgents, (agentIndex+1)%numOfAgents, alpha, beta)
                chooseMin.append(res[0])
                # Check "cut-off" condition
                if min(chooseMin) < beta:  # If beta is larger than the current Min value
                    beta = min(chooseMin) # Then replace beta with the current Min value
                if alpha >= beta: # When alpha value is larger than beta value
                    return alpha  #alpha cut-off

        # Case 3. If there are more ghosts left then call minValue for Ghost agent
        else:
            for nextState in nextStates:
                res = self.minValueAlphaBeta(nextState, depth-1, numOfMins-1, numOfAgents, (agentIndex+1)%numOfAgents, alpha, beta)
                chooseMin.append(res)
                # Check "cut-off" condition
                if min(chooseMin) < beta: # If beta is larger than the current Min value
                    beta = min(chooseMin) # Then replace beta with the current Min value
                if alpha >= beta: # When alpha value is larger than beta value
                    return alpha  #alpha cut-off

        return min(chooseMin)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

