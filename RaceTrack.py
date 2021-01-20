import numpy as np
from pygame import *
import pygame
from Car import Car
import sys
import time

goalColor = Color(168, 50, 50)
startColor = Color(26, 163, 8)
wallColor = Color(0, 0, 0)
nullColor = Color(255, 255, 255)
carColor = Color(14, 19, 161)


class RaceTrack:
	"""
	This class defines the racetrack for the car to drive on
	"""

	def __init__(self, size=60, scale=10):

		# Create clock
		self.size = size
		self.scale = scale

		# Set up the backend track
		self.goal = (2, 2)
		self.start = (size - 3, size - 3)
		self.track = np.zeros((size, size))

		# Set up the user side track
		pygame.init()
		self.clock = pygame.time.Clock()

		# Initialize Screen
		self.screen = self.blankScreen()

	def blankScreen(self):

		scale = self.scale
		size = self.size

		# Open a window on the screen
		screen_width = size * scale
		screen_height = size * scale
		screen = pygame.display.set_mode([screen_width, screen_height])
		screen.fill(nullColor)

		# Draw the start and the end
		screenGoal = Rect(scale, scale, scale * 3, scale * 3)
		screenStart = Rect(size * scale - (4 * scale), size * scale - (4 * scale),
		                   scale * 3, scale * 3)

		draw.rect(screen, startColor, screenStart)
		draw.rect(screen, goalColor, screenGoal)

		display.flip();

		return screen

	def updateScreen(self, rect=None):
		display.update(rect)
		pygame.event.get()
		self.clock.tick()

	def visualRectangle(self, trackCoor, size):
		"""Creates a rectangle that is to scale with the visual"""

		screenPos = [(x * self.scale) - (x * self.scale) % self.scale for x in trackCoor]
		return Rect(screenPos[0], screenPos[1], self.scale * size, self.scale * size)

	def addTrackWall(self, location):
		if self.track[location[0]][location[1]] == 1:
			return False
		self.track[location[0]][location[1]] = 1
		return True

	def addWall(self, position):
		"""
		Adds a wall to the race track
		:param position:
		:return:
		"""

		# Find the position in terms of the track
		trackPos = [(x // self.scale) for x in position]

		# If you do not already have a wall placed place one
		if self.addTrackWall(trackPos):

			# Add the scaled wall to the screen
			rect = self.visualRectangle(trackPos, 1)
			draw.rect(self.screen, wallColor, rect)
			self.updateScreen(rect)

	def addWalls(self):
		"""
		Collects all user entered walls well their mouse is held down and adds them to the track
		:param self: The RaceTrack
		"""

		pygame.event.set_blocked(None)
		pygame.event.set_allowed(MOUSEBUTTONUP)

		running = True
		while running:

			# If the user stops holding down the mouse
			if len(pygame.event.get()):
				break

			self.addWall(mouse.get_pos())

		pygame.event.set_allowed(None)

	def clearTrack(self):
		self.track = np.zeros((self.size, self.size))
		self.screen = self.blankScreen()

	def addPath(self, ai):
		"""
		Adds a path to the visualization using the specified ai algorithm
		:param ai: The ai algorithm used to add the path
		"""

		def numSplit(number, parts):
			"""
			Splits a number into an array of size parts of roughly equal values
			Used to figure how many frames should be used for each move
			i.e. numSplit(10, 2) = [5, 5]

			:param number: The number to split
			:param parts: The # of ~parts to split the number into
			:return: The array of ~parts
			"""
			div = number // parts
			return_array = [div] * parts
			rem = number % parts
			for i in range(rem):
				return_array[i] += 1
			return return_array

		# Get the path from the passed in ai
		path = ai(self)

		# Begin printing the path to the screen
		print("Get Ready for it:")
		time.sleep(5)

		# Iterate through each move given by the AI
		for move in path:
			positionTime = numSplit(60, len(move))

			# Iterate through each position of the given move
			for i in range(len(move)):
				rect = self.visualRectangle(move[i], 1)
				draw.rect(self.screen, carColor, rect)
				self.updateScreen(rect)

				# Sleep for amount of move execution time
				for j in range(positionTime[i]):
					time.sleep(.00166666666666667)
