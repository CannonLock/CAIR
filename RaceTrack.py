import numpy as np
from Car import Car
import sys

class RaceTrack:

    def __init__(self, start, goal, size):
        self.goal = goal
        self.start = start
        self.cars = []
        self.size = size
        self.track = np.zeros((size,size))

    def addWall(self, location):
        if self.track[location[0]][location[1]] == 1:
            return False
        self.track[location[0]][location[1]] = 1
        return True

    def removeWall(self, location):
        self.track[location[0]][location[1]] = 0

    def clearTrack(self):
        self.track = np.zeros((self.size, self.size))

    def updateEdges(self, car):
        edges = []
        carPosR, carPosC = car.getPosition()

        # N
        i = carPosR
        distance = 0
        while i >= 0:
            if(self.track[i][carPosC] == 1):
                edges.append(distance)
                break
            distance += 1
            i -= 1
        if len(edges) != 1:
            edges.append(sys.maxsize)

        # NE
        i = carPosR
        j = carPosC
        distance = 0
        while i >= 0 and j < self.size:
            if(self.track[i][j] == 1):
                edges.append(distance)
                break
            distance += 1
            i -= 1
            j += 1
        if len(edges) != 2:
            edges.append(sys.maxsize)

        # E
        j = carPosC
        distance = 0
        while j < self.size:
            if(self.track[carPosR][j] == 1):
                edges.append(distance)
                break
            distance += 1
            j += 1
        if len(edges) != 3:
            edges.append(sys.maxsize)

        # SE
        i = carPosR
        j = carPosC
        distance = 0
        while i < self.size and j < self.size:
            if (self.track[i][j] == 1):
                edges.append(distance)
                break
            distance += 1
            i += 1
            j += 1
        if len(edges) != 4:
            edges.append(sys.maxsize)

        # S
        i = carPosR
        distance = 0
        while i < self.size:
            if (self.track[i][carPosC] == 1):
                edges.append(distance)
                break
            distance += 1
            i += 1
        if len(edges) != 5:
            edges.append(sys.maxsize)

        # SW
        i = carPosR
        j = carPosC
        distance = 0
        while i < self.size and j >= 0:
            if (self.track[i][j] == 1):
                edges.append(distance)
                break
            distance += 1
            i += 1
            j -= 1
        if len(edges) != 6:
            edges.append(sys.maxsize)

        # W
        j = carPosC
        distance = 0
        while j >= 0:
            if(self.track[carPosR][j] == 1):
                edges.append(distance)
                break
            distance += 1
            j -= 1
        if len(edges) != 7:
            edges.append(sys.maxsize)

        # NW
        i = carPosR
        j = carPosC
        distance = 0
        while i >= 0 and j >= 0:
            if (self.track[i][j] == 1):
                edges.append(distance)
                break
            distance += 1
            i -= 1
            j -= 1
        if len(edges) != 8:
            edges.append(sys.maxsize)

        # Update the cars internal edge measurements
        car.updateEdges(edges)





