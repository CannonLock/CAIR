import heapq as hq


class PriorityQueue:
	"""
	A priority queue using a heap and a dictionary for quick retrieval of the top option and
	"""

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
