from RaceTrack import *
import pygame
import AI
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *

def main(size, scale):

	# Initialize a new track
	track = RaceTrack(size, scale)

	# Begin the user input loop
	running = True
	while running:

		# Check and process event queue
		for event in pygame.event.get():

			# On click add walls
			if event.type == pygame.MOUSEBUTTONDOWN:
				track.addWalls()

			if event.type == pygame.KEYDOWN:

				# On enter run the algorithm on the current track
				if event.__dict__['unicode'] == '\r':
					track.addPath(AI.AStar);

				# On delete clear the board for a new run
				if event.__dict__['unicode'] == '\b':
					track.clearTrack();


			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False

if __name__ == '__main__':

	while True:

		# Initialize the default
		userInts = (60, 10)

		# Ask for user input
		userVariables = input(
			"\n\n"
			"Welcome to CAIR!\n"
			"To interact with the UI upon parameter entry use the following commands:\n"
			"Click and Hold: Draw walls that the car must navigate around\n"
			"Enter: Run the pathfinding algorithm and trace the cars path\n"
			"Delete: Remove the current path and draw a new one\n\n"
			"You can choose to use custom size and scale parameters or press enter for the default.\n"
			"I have found a size of 60 to be a sweet spot where you can have many obstacles and \n"
			"sub minute runtimes on a slow laptop processor.\n"
			"\n"
			"Press Enter for default, or input size and scale in form '60 10':"
		).split(" ")

		# Check for default and print if chosen
		if userVariables == ['']:
			print("60 10")
			break

		try:
			userInts = list(map(lambda x : int(x), userVariables))
		except:
			print("All values must be castable to integers")

		if len(userInts) == 2:
			break

		elif len(userInts) != 2:
			print("Invalid # of parameters")

	main(*userInts)