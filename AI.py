import heapq as hq
import numpy as np
from math import *

#make life easier
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

def genPossMoves(state, moveArr):
    """
    Generates the array of all valid next moves for the input car state

    :param state: {'h': heuristic, 'g': moves to this position, 'f': g(n) + h(n),
               'state': ((position tuple), velocity, angle), 'parent': state}
    :return: An array of possible next moves
    """
    v = state['state'][1]
    a = state['state'][2]

    # all v = 1 moves valid for stopped car
    if v == 0:
        return moveArr[1]

    # when v > 0
    positionRatio = a / (2 * pi)
    possMoves = []
    # adjacent distances
    for i in (0, -1, 1):
        if v + i < 0 or v + i > 6:
            continue
        if v + i == 0:
            possMoves.append((0,0))
            continue
        currAlignment = round(positionRatio * len(moveArr[v + i]))

        # adjacent turns
        for j in (0, -1, 1):
            if currAlignment + j == len(moveArr[v + i]):
                j = 0
            elif currAlignment + j < 0:
                j = len(moveArr[v + i]) - 1
            possMoves.append(moveArr[v + i][currAlignment + j])

    return possMoves

def genMoveReferenceArray():
    """
    Generates the array that contains all move offsets for a specific velocity
    :return: referenceArray
    """

    def mergeSortDict(arr):
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

    type = 0

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

def radianDif(r0, r1):
    dif = abs(r0 - r1)
    if dif > pi:
        return 2 * pi - dif
    else:
        return dif

def calcF(g, h):
    return g + h

def calcG(parentG):
    return parentG + 1

def calcH(state, goal):
    currPos = state[0]
    euclidean = round(sqrt((currPos[0] - goal[0]) ** 2 + (currPos[1] - goal[1]) ** 2) / 7)
    moveVector = tupleSubtract(goal, currPos)
    a = atan2(moveVector[0], moveVector[1])
    angleEffect = (1/10) - ((radianDif(a, state[2]) / pi)*1/10)
    return euclidean - angleEffect

def findSuccessorStates(track, state, moveArr):
    """
    Finds all states that can follow the input
    :param state: {'h': heuristic, 'g': moves to this position, 'f': g(n) + h(n),
                   'state': np.array(), 'parent': state}
    :return: All states that can succeed this one
    """

    succStates = []

    possMoves = genPossMoves(state, moveArr)
    for move in possMoves:
        parentPos = state['state'][0]
        currPos = tupleAdd(state['state'][0], move)
        moveArray = genMoveArray(parentPos, currPos)
        hitWall = False
        for pos in moveArray:
            if (pos[0] < 0 or pos[0] >= track.size) or (pos[1] < 0 or pos[1] >= track.size):
                hitWall = True
                break
            if track.track[int(pos[0])][int(pos[1])] == 1:
                hitWall = True
                break

        if not hitWall:

            moveVector = tupleSubtract(currPos, parentPos)
            v = round(hypot(moveVector[0], moveVector[1]))
            a = round(atan2(moveVector[0], moveVector[1]), 2)
            if a < 0:
                a = a + 2 * pi
            stateTuple = (tuple(currPos), v, a)
            if state['parent'] == None:
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

class PriorityQueue():

    def __init__(self):
        self.heap = []
        self.queue = {}
        self.entry = 0
        self.max_len = 0

    def __str__(self):
        return str(self.queue)

    def getEntryNumber(self):
        temp = self.entry
        self.entry += 1
        return temp

    def isEmpty(self):
        return len(self.queue) == 0

    def enqueue(self, car_dict):
        """
        - All items in the queue are dictionaries
            'state' = ((position tuple), velocity, angle)
            'h' = heuristic value
            'parent' = reference to the previous state
            'g' = the number of more to get to this state from initial
            'f' = g(n) + h(n)
        """
        in_open = False

        # search for duplicate states
        if car_dict["state"] in self.queue:

            in_open = True

            if self.queue[car_dict["state"]]["g"] > car_dict["g"]:
                # remove old item
                oldState = self.queue.pop(car_dict["state"])
                oldState['r'] = 1
                # add new
                self.queue[car_dict["state"]] = car_dict
                hq.heappush(self.heap, (car_dict['f'], self.getEntryNumber(), car_dict))

        if not in_open:
            self.queue[car_dict["state"]] = car_dict
            hq.heappush(self.heap, (car_dict['f'], self.getEntryNumber(), car_dict))

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        # re add the dict to the queue
        self.queue[from_closed["state"]] = from_closed

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """

        while True:
            priority, count, state = hq.heappop(self.heap)
            if state['state'] in self.queue and 'r' not in state:
                # delete and return the min dictionary
                del self.queue[state['state']]
                return state

def AStarRaceCar(track):
    """
    Uses A* search to find a path for the car
    :param track: the track data
    :return: An array of moves for the car to make to reach the goal
    """
    def solve():

        def getSolution(goalState):
            moveList = []

            while goalState['parent'] != None:
                moveList.append(genMoveArray(goalState["parent"]['state'][0], goalState['state'][0]))
                goalState = goalState["parent"]

            return list(reversed(moveList))

        moveArr = genMoveReferenceArray()

        openQueue = PriorityQueue()
        closed = {}
        goal = track.goal

        openQueue.enqueue({'state': (track.start, 0, 0), 'parent': None,
                           'f': 0 + calcH((track.start, 0, 0), track.goal), 'g': 0,
                           'h': calcH((track.start, 0, 0), track.goal)})

        while(not openQueue.isEmpty()):
            currState = openQueue.pop()
            closed[currState['state']] = currState

            if(currState['state'][0] == goal):
                return getSolution(currState)

            else:
                succStates = findSuccessorStates(track, currState, moveArr)

                for state in succStates:

                    if state['state'] in closed:

                        if closed[state['state']]['g'] > state['g']:

                            del closed[state['state']]
                            openQueue.enqueue(state)

                    else:

                        openQueue.enqueue(state)

        print("FAILURE : F in the chat")

    return solve()

