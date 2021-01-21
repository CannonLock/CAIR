import heapq as hq
import random

class PriorityQueue:
	"""
	A priority queue using a heap and a dictionary for quick retrieval of the top option and
	"""

	def __init__(self):
		self.heap = []
		self.queue = {}
		self.max_len = 0

		# Establish tie breaking system policies
		self.randomIdList = random.sample(range(10000), 10000)
		self.maxId = 10000

	def __str__(self):
		return str(self.queue)

	def getEntryNumber(self):

		if len(self.randomIdList) == 0:
			self.randomIdList = random.sample(range(self.maxId, self.maxId + 10000), 10000)
			self.maxId = self.maxId + 10000

		return self.randomIdList.pop()

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

	def pop(self):
		"""
		Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
		"""

		while True:
			priority, count, state = hq.heappop(self.heap)
			if state['state'] in self.queue:

				# Delete current entry
				del self.queue[state['state']]

				# If it has not been removed return the state
				if 'r' not in state:
					return state
