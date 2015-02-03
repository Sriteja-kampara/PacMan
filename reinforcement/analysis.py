# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

# Low Noise guarantees to the direction to go across the bridge
# It worked when answerNoise value is the range from 0.00 to 0.01.
def question2():
  answerDiscount = 0.9
  answerNoise = 0.001
  return answerDiscount, answerNoise

# Prefer the close exit (+1), risking the cliff (-10)
# Small discount so that the agent chooses the exit (+1)
def question3a():
  answerDiscount = 0.1
  answerNoise = 0.0
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

# Prefer the close exit (+1), but avoiding the cliff (-10)
# Small discount so that the agent chooses the exit (+1)
# and negative LivingReward so that the agent avoids the cliff
def question3b():
  answerDiscount = 0.3
  answerNoise = 0.2
  answerLivingReward = -1
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

# Prefer the distant exit (+10), risking the cliff (-10)
# Similar to the case 3a(), but large Discount value to choose the exit (+10)
def question3c():
  answerDiscount = 0.9
  answerNoise = 0.0
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

# Prefer the distant exit (+10), avoiding the cliff (-10)
# large discount and LivingReward with a small noise both to go distant exit and to avoid the cliff
def question3d():
  answerDiscount = 0.9
  answerNoise = 0.1
  answerLivingReward = 0.99
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

# Avoid both exits (also avoiding the cliff)
# If all values are 0, then the iterations come to nothing
# Therefore the agent avoid both exits
def question3e():
  answerDiscount = 0.0
  answerNoise = 0.0
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = None
  answerLearningRate = None
  return 'NOT POSSIBLE'
  # If not possible, return 'NOT POSSIBLE'
  
if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
