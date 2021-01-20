from PriorityQueue import *
import numpy as np
from math import *

"""
    These functions are to make like easier
"""
def tupleAdd(t0, t1):
	r = []
	i = 0
	while i < len(t0):
		r.append(t0[i] + t1[i])
		i += 1
	return tuple(r)

def tupleSubtract(t0, t1):
	r = []
	i = 0
	while i < len(t0):
		r.append(t0[i] - t1[i])
		i += 1
	return tuple(r)

def genMoveArray(start, end):
	"""
	Creates a array that maps a move from start to end
	:param start: Start pos
	:param end: End pos
	:return: Array of positions the car enters during the move
	"""

	def numSplit(num, parts):
		div = num // parts
		return_array = [div] * parts
		rem = num % parts
		for i in range(rem):
			return_array[i] += 1
		return return_array

	move = tupleSubtract(end, start)
	currPos = list(start)

	if abs(move[0]) > abs(move[1]):
		p = (0, 1)
	else:
		p = (1, 0)

	arr = numSplit(abs(move[p[0]]), abs(move[p[1]]) + 1)
	retArr = [start]

	i = 0
	while True:

		# Do
		for increment in range(arr[i]):
			currPos[p[0]] += move[p[0]] / abs(move[p[0]])
			retArr.append((currPos[0], currPos[1]))

		# While
		if i > (len(arr) - 2):
			break

		currPos[p[1]] += move[p[1]] / abs(move[p[1]])
		retArr.append((currPos[0], currPos[1]))
		i += 1

	return retArr

def genPossMoves(state, referenceArray):
	"""
	Generates the array of all valid next moves for the input car state

	:param state: {'h': heuristic, 'g': moves to this position, 'f': g(n) + h(n),
	         'state': ((position tuple), velocity, angle), 'parent': state}
	:param moveArray: Passed in reference array of possible moves at each speed
	:return: An array of possible next moves
	"""
	position, velocity, angle = state['state']

	# all velocity = 1 moves valid for stopped car
	if velocity == 0:
		return referenceArray[1]

	# when velocity > 0
	positionRatio = angle / (2 * pi)
	possibleMoves = []

	# adjacent distances
	for i in (0, -1, 1):

		# If the new velocity is invalid
		if velocity + i < 0 or velocity + i > 6:
			continue

		if velocity + i == 0:
			possibleMoves.append((0, 0))
			continue

		# Find the most closely representative square at this speed and angle

		currentAlignment = round(positionRatio * len(referenceArray[velocity + i]))

		# adjacent turns
		for j in (0, -1, 1):

			# If end of list is reached wrap to first item
			if currentAlignment + j == len(referenceArray[velocity + i]):
				j = 0

			elif currentAlignment + j < 0:
				j = len(referenceArray[velocity + i]) - 1

			possibleMoves.append(referenceArray[velocity + i][currentAlignment + j])

	return possibleMoves


def genMoveReferenceArray(type):
	"""
	Generates the array that contains all move offsets for a specific velocity
	:param type: Dictates the function used to calculate the integer value (round, ceil, floor)
	:return: A reference array to be used to calculate successors
	"""

	def mergeSortDict(arr):
		"""
		Recursive function to do a merge sort
		! Very unnecessary optimization !
		:param arr: The array to sort
		:return: The sorted array
		"""
		if len(arr) > 1:
			mid = len(arr) // 2
			L = arr[:mid]
			R = arr[mid:]

			mergeSortDict(L)
			mergeSortDict(R)
			i = j = k = 0

			# Copy data to temp arrays L[] and R[]
			while i < len(L) and j < len(R):
				if list(L[i].keys())[0] < list(R[j].keys())[0]:
					arr[k] = L[i]
					i += 1
				else:
					arr[k] = R[j]
					j += 1
				k += 1

			# Checking if any element was left
			while i < len(L):
				arr[k] = L[i]
				i += 1
				k += 1

			while j < len(R):
				arr[k] = R[j]
				j += 1
				k += 1

	moveArr = [[] for i in range(7)]

	if type == 0:
		for x in range(13):
			for y in range(13):
				adjPos = np.array([6, 6]) - np.array([x, y])
				if (round(hypot(adjPos[1], adjPos[0])) < 7):
					d = round(hypot(adjPos[1], adjPos[0]))
					a = round(atan2(adjPos[0], adjPos[1]), 2)
					if a < 0:
						a = a + 2 * pi
					moveArr[d].append({a: tuple(adjPos)})

	if type == 1:
		for x in range(13):
			for y in range(13):
				adjPos = np.array([6, 6]) - np.array([x, y])
				if (ceil(hypot(adjPos[1], adjPos[0])) < 7):
					d = round(hypot(adjPos[1], adjPos[0]))
					a = round(atan2(adjPos[0], adjPos[1]), 2)
					if a < 0:
						a = a + 2 * pi
					moveArr[d].append({a: tuple(adjPos)})

	if type == 2:
		for x in range(13):
			for y in range(13):
				adjPos = np.array([6, 6]) - np.array([x, y])
				if (floor(hypot(adjPos[1], adjPos[0]), 0) < 7):
					d = round(hypot(adjPos[1], adjPos[0]))
					a = round(atan2(adjPos[0], adjPos[1]), 2)
					if a < 0:
						a = a + 2 * pi
					moveArr[d].append({a: tuple(adjPos)})

	for d in range(7):
		mergeSortDict(moveArr[d])
		moveArr[d] = [innerDict.popitem()[1] for innerDict in moveArr[d]]

	return moveArr


def calcF(g, h):
	return g + h


def calcG(parentG):
	return parentG + 1


def calcH(state, goal):
	"""
	Calculate the heuristic value of the current state
	:param state: The given car state
	:param goal: The location of the goal
	:return: The heuristic value
	"""
	currentPosition = state[0]

	goalVector = tupleSubtract(goal, currentPosition)

	distanceFromGoal = hypot(*goalVector)

	minimumMoves = floor(distanceFromGoal / 12.8)
	print(minimumMoves)
	return minimumMoves


def hitsWall(currentPosition, parentPosition, track):
	"""
	Check if during the move from the parent to the current position a wall is present
	:param currentPosition: The current position
	:param parentPosition: The previous position
	:param track: The array that contains the wall locations
	:return: True if it hits a wall, else false
	"""

	# Generate the spaces this move will occupy
	moveArray = genMoveArray(parentPosition, currentPosition)

	# Iterate through spaces moved through and check if a wall occupies it
	hitWall = False
	for pos in moveArray:
		if (pos[0] < 0 or pos[0] >= track.size) or (pos[1] < 0 or pos[1] >= track.size):
			hitWall = True
			break
		if track.track[int(pos[0])][int(pos[1])] == 1:
			hitWall = True
			break

	return hitWall


def findSuccessorStates(track, state, moveArr):
	"""
	Finds all states that can follow the input
	:param state: {'h': heuristic, 'g': moves to this position, 'f': g(n) + h(n),
	             'state': np.array(), 'parent': state}
	:return: All states that can succeed this one
	"""
	possMoves = genPossMoves(state, moveArr)

	# Generate all of the possible successor states
	succStates = []

	for move in possMoves:

		parentPosition = state['state'][0]
		currentPosition = tupleAdd(state['state'][0], move)

		if not hitsWall(currentPosition, parentPosition, track):

			v = round(hypot(*move))
			a = round(atan2(move[0], move[1]), 2)

			# Make sure that the angle is positive
			if a < 0:
				a = a + 2 * pi

			stateTuple = (tuple(currentPosition), v, a)

			if state['parent'] is None:
				g = 0
			else:
				g = calcG(state['parent']['g'])

			h = calcH(stateTuple, track.goal)
			f = calcF(g, h)

			succStates.append(
				{
					'state': stateTuple,
					'h': h,
					'g': g,
					'f': f,
					'parent': state
				}
			)

	return succStates


def getSolution(goalState):
	"""
	Traces the path of the given state from the goal back to the start
	:param goalState: The state that ends the optimal path
	:return: An array of arrays were each inner array represents the tile moves in one piece of time
	"""
	moveList = []

	while goalState['parent'] != None:
		moveList.append(genMoveArray(goalState["parent"]['state'][0], goalState['state'][0]))
		goalState = goalState["parent"]

	print("Solution is ", len(moveList), " steps long!")

	return list(reversed(moveList))


def AStar(track):
	"""
	Uses A* search to find a path for the car
	:param track: the track data
	:return: An array of moves for the car to make to reach the goal
	"""

	# Pre-Generate the move reference array
	referenceArray = genMoveReferenceArray(0)

	openQueue = PriorityQueue()
	closed = {}
	goal = track.goal

	openQueue.enqueue({
		'state': (track.start, 0, 0),
		'parent': None,
		'f': 0 + calcH((track.start, 0, 0), track.goal),
		'g': 0,
		'h': calcH((track.start, 0, 0), track.goal)
	})

	while (not openQueue.isEmpty()):

		currentState = openQueue.pop()
		closed[currentState['state']] = currentState

		if (currentState['state'][0] == goal):
			return getSolution(currentState)

		else:
			succStates = findSuccessorStates(track, currentState, referenceArray)

			for state in succStates:

				if state['state'] in closed:

					if closed[state['state']]['g'] > state['g']:
						del closed[state['state']]
						openQueue.enqueue(state)

				else:

					openQueue.enqueue(state)

	raise Exception("Error: No Path Found")
