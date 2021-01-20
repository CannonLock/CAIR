from RaceTrack import *
import pygame
import AI
from pygame import *

def main():

	# Initialize a new track
	track = RaceTrack()

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
	main()