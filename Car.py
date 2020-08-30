import numpy as np
from math import *


def genMoveDict():
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
        moveArr[d] = [list(innerDict.values())[0] for innerDict in moveArr[d]]

    return moveArr

# Holds all information that pertains to each individual car
class Car:

    moveDict = genMoveDict()

    def __init__(self, position = [0,0]):
        self.position = position
        self.a = 0
        self.v = 0

    def updatePosition(self):
        self.position = map(sum, [self.velocity*x for x in self.direction], self.position)

    def updateEdges(self, edges):
        self.edges = edges

    def right(self):
        if self.position[0] < self.position[1]:
            if sum(self.position) == 2:
                self.direction = map(sum, self.direction, [1,-1])
            if self.direction[1] >= 0:
                self.direction = map(sum, self.direction, [1,1])
        else:
            if sum(self.position) == -2:
                self.direction = map(sum, self.direction, [-1, 1])
            else:
                self.direction = map(sum, self.direction, [-1, -1])

    def left(self):
        if self.position[0] < self.position[1]:
            if sum(self.position) == -2:
                self.direction = map(sum, self.direction, [1,-1])
            if self.direction[0] < 1:
                self.direction = map(sum, self.direction, [-1,-1])
        else:
            if sum(self.position) == 2:
                self.direction = map(sum, self.direction, [-1, 1])
            else:
                self.direction = map(sum, self.direction, [1, 1])

    def velocityUp(self):
        if self.velocity < 5:
            self.velocity += 1

    def velocityDown(self):
        if self.velocity >= 0:
            self.velocity -= 1

    def getPosition(self):
        return self.position

    def genPossMoves(self):
        """
        Generates the array of all valid next moves for the input car

        :param car: The car that is going to move
        :return: An array of possible next moves
        """
        # all v = 1 moves valid for stopped car
        if self.v == 0:
            return moveDict[1]

        # when v > 0
        positionRatio = self.a / 2 * pi
        possMoves = []
        # adjacent distances
        for i in range(-1, 2):
            if self.v + i < 0 or self.v + i > 6:
                continue
            elif self.v + i == 0:
                possMoves.append([0, 0])
                continue
            currAlignment = round(positionRatio * len(moveDict[self.v + i]))
            # adjacent turns
            for j in range(-1, 2):
                if currAlignment + j > len(moveDict[self.v + i]):
                    j = 0
                elif currAlignment + j < 0:
                    j = len(moveDict[self.v + i]) - 1
                possMoves.append(moveDict[self.v + i][currAlignment + j])

        return possMoves
