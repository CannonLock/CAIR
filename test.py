import numpy as np
import time
from math import *
import AI as ai





# pos to pos movement array and its visualization
def moveArray(start, end):
    def numSplit(num, parts):
        div = num // parts
        return_array = [div] * parts
        rem = num % parts
        for i in range(rem):
            return_array[i] += 1
        return return_array

    move = end - start
    currPos = start.copy()
    if abs(move[0]) > abs(move[1]):
        p = (0,1)
    else:
        p = (1,0)

    arr = numSplit(abs(move[p[0]]), abs(move[p[1]]) + 1)
    retArr = []

    i = 0
    while True:
        #Do
        for increment in range(arr[i]):
            currPos[p[0]] += move[p[0]]/abs(move[p[0]])
            retArr.append((currPos[0], currPos[1]))
        #While
        if i > (len(arr) - 2):
            break
        currPos[p[1]] += move[p[1]]/abs(move[p[1]])
        retArr.append((currPos[0], currPos[1]))
        i +=1
    return retArr

def moveVis(start, end):
    space = np.zeros((11, 11))
    space[start[0]][start[1]] = 1
    space[end[0]][end[1]] = 9

    arr = moveArray(start, end)

    for move in arr:
        space[move[0]][move[1]] = 5

    print(space)

# non-relative move array and its visualization
def genMoveArr():
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

    for x in range(13):
        for y in range(13):
            adjPos = np.array([6, 6]) - np.array([x, y])
            if (round(hypot(adjPos[1], adjPos[0]), 0) < 7):
                d = round(hypot(adjPos[1], adjPos[0]))
                a = round(atan2(adjPos[0], adjPos[1]), 2)
                if a < 0:
                    a = a + round(2 * pi, 2)
                moveArr[d].append({a: adjPos.tolist()})

    for d in range(7):
        mergeSortDict(moveArr[d])
        print(moveArr[d])
        moveArr[d] = [list(innerDict.values())[0] for innerDict in moveArr[d]]

    return moveArr

def moveCircleVis(type, radius):

    ad = np.zeros((13,13))
    aa = np.zeros((13,13))
    ad[6][6] = aa[6][6] = 1
    circleDict = {'angle' : []}
    c = np.array([6,6])

    if(type == 0):
        for x in range(13):
            for y in range(13):
                adjPos = c - np.array([x,y])
                if(round(hypot(adjPos[1], adjPos[0]), 0) == radius):
                    d = round(hypot(adjPos[0], adjPos[1]), 2)
                    a = round(atan2(adjPos[0], adjPos[1]), 2)
                    if a < 0:
                        a = a + 2*pi
                    circleDict[a] = (adjPos[0], adjPos[1])
                    ad[y][x] = d
                    aa[y][x] = a

    if (type == 1):
        for x in range(13):
            for y in range(13):
                adjPos = c - np.array([x, y])
                if (ceil(hypot(adjPos[1], adjPos[0])) == radius):
                    d = round(hypot(adjPos[0], adjPos[1]), 2)
                    a = round(atan2(adjPos[0], adjPos[1]), 2)
                    if a < 0:
                        a = a + 2 * pi
                    circleDict[a] = (adjPos[0], adjPos[1])
                    ad[y][x] = d
                    aa[y][x] = a

    if (type == 2):
        for x in range(13):
            for y in range(13):
                adjPos = c - np.array([x, y])
                if (floor(hypot(adjPos[1], adjPos[0])) == radius):
                    d = round(hypot(adjPos[0], adjPos[1]), 2)
                    a = round(atan2(adjPos[0], adjPos[1]), 2)
                    if a < 0:
                        a = a + 2 * pi
                    circleDict[a] = (adjPos[0], adjPos[1])
                    ad[y][x] = d
                    aa[y][x] = a


    np.set_printoptions(linewidth=100, precision=2)
    print(ad, "\n", aa)


def genPossMoves(state):
    """
    Generates the array of all valid next moves for the input car state

    :param state: The state of a car that is going to move {'v':?, 'a':?, 'p':?}
    :return: An array of possible next moves
    """
    # all v = 1 moves valid for stopped car
    if state['v'] == 0:
        return moveDict[1]

    # when v > 0
    positionRatio = state['a'] / 2 * pi
    possMoves = []
    # adjacent distances
    for i in range(-1,2):
        if state['v'] + i < 0 or state['v'] + i > 6:
            continue
        elif state['v'] + i == 0:
            possMoves.append([0,0])
            continue
        currAlignment = round(positionRatio * len(moveDict[state['v'] + i]))
        # adjacent turns
        for j in range(-1,2):
            if currAlignment + j > len(moveDict[state['v'] + i]):
                j = 0
            elif currAlignment + j < 0:
                j = len(moveDict[state['v'] + i]) - 1
            possMoves.append(moveDict[state['v'] + i][currAlignment + j])

    return possMoves



if __name__ == '__main__':
    moveDict = genMoveArr()
    referenceArray = ai.genMoveReferenceArray()

    for i in range(6):
        moveCircleVis(0, i)



