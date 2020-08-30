import unittest
from random import *
import AI as ai
from RaceTrack import *
from math import *

class TestAI(unittest.TestCase):

    def test_queue_norm(self):
        queue = ai.PriorityQueue()

        queue.enqueue({'h': 0, 'g': 0, 'f': 1, 'state': ((1, 0), 0, 0), 'parent': None})

        for i in range(5):
            for j in range(100):
                queue.enqueue({'h': 0, 'g' : 1, 'f' : uniform(10,40), 'state' : ((j,0),0,0), 'parent' : None})

        queue.enqueue({'h': 0, 'g': 0, 'f': 1, 'state': ((1, 0), 0, 0), 'parent': None})

        self.assertEqual(len(queue.queue), 100)

    def test_succ_states(self):
        size = 50
        track = RaceTrack((size - 3, size - 3), (2, 2), size)
        referenceMoveArray = ai.genMoveReferenceArray()

        for i in range(1, 13):
            state = {'h': 0, 'g': 0, 'f': 1, 'state': ((1, 1), 2, (2*pi)/i - .01), 'parent': None}
            succStates = ai.findSuccessorStates(track, state, referenceMoveArray)
            for state in succStates:
                print(state)




        self.assertEqual(True, True)




if __name__ == '__main__':
    unittest.main()