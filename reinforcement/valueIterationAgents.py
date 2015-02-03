# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

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
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0

    "*** YOUR CODE HERE ***"

    allStates =  mdp.getStates()

    for i in range(0, iterations) :
        print "================>    Iteration [", i+1, "]   <================ "
        # Declare a temporary value dictionary to store the values for the next iteration
        iterationValues = self.values.copy()
        for eachState in allStates :
            maxValue = -99999
            # Compute [V(s) = max Q value] for each (action, state) per the iteration
            for eachAction in mdp.getPossibleActions(eachState) :
                # print "    State:", eachState, "Action:", eachAction, "Q value:", self.getQValue(eachState, eachAction)
                currentQValue = self.getQValue(eachState, eachAction)
                if (currentQValue >= maxValue) :
                    maxValue = currentQValue
                    iterationValues[eachState] = currentQValue
        # Copy updated values to the original value list
        #   so that the next iteration can make a reference (Dynamic Programming)
        self.values = iterationValues.copy()
        print self.values

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"

    # Q Value is the expected utility having taken action "a" from state "s" to "s'"
    # Q value = [sum of (T(s,a,s')*{R(s,a,s')+(r*V(s'))}] where
    # T(s,a,s'): the probability for the next state with a certain action = mdp.getTransitionStatesAndProbs(state, action)
    # R(s,a,s'): the reward for the next state with a certain action = mdp.getReward(state, action, nextState)
    # r or gamma: self.discount, V(s'): v value of next state

    qValue = 0.0
    currentTransitionInfo = self.mdp.getTransitionStatesAndProbs(state, action)

    for (nextState, nextStateProb) in currentTransitionInfo :
        # print "(nextState, nextStateProb, Reward) = (",nextState, ",",nextStateProb, ",", self.mdp.getReward(state, action, nextState), ")"
        qValue +=  nextStateProb * (self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))

    # Returns the q-value of the (state, action) pair
    return qValue

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"

    # If the given state is a terminal one, then return None
    if self.mdp.isTerminal(state) :
        return None

    # Get the all possible actions with qValue
    # And then return the action which represents the maximum argument
    else :
        actionList = util.Counter()
        actions = self.mdp.getPossibleActions(state)
        for action in actions:
            actionList[action] = self.getQValue(state, action)
        return actionList.argMax()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
