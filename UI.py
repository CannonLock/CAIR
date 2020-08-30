from RaceTrack import *
import pygame
import AI
from pygame import *
import time
import time
from multiprocessing import Pool

# Colors
goalColor = Color(168, 50, 50)
startColor = Color(26, 163, 8)
wallColor = Color(0, 0, 0)
nullColor = Color(255, 255, 255)
carColor = Color(14, 19, 161)

# Create clock
clock = pygame.time.Clock()

def addPath(track, scale, screen):

    def numSplit(num, parts):
        div = num // parts
        return_array = [div] * parts
        rem = num % parts
        for i in range(rem):
            return_array[i] += 1
        return return_array

    path = AI.AStarRaceCar(track)
    print("Get Ready for it:")
    time.sleep(5)
    for moves in path:
        frames = numSplit(60, len(moves))

        i = 0
        while i < len(moves):
            rect = uiRectangle(moves[i], scale, 1)
            draw.rect(screen, carColor, rect)
            updateScreen(rect)

            j = 0
            while j < frames[i]:
                time.sleep(.00166666666666667)
                j += 1

            i += 1

def addWalls(track, scale, screen):
    '''
    Runs the wall addition loop that updates on mouse up
    :param track: The Racetrack
    :param screen: The Screen
    '''

    def addWall(track, scale, screen, position):
        '''
        Displays a wall and updates the racetrack

        :param track: The Racetrack
        :param screen: The display
        :param position: The positions of the mouse
        '''

        # Find the position in terms of the track
        trackPos = [(x // scale) for x in position]
        if track.addWall(trackPos):

            # Add the wall
            rect = uiRectangle(trackPos, scale, 1)
            draw.rect(screen, wallColor, rect)
            updateScreen(rect)

    pygame.event.set_blocked(None)
    pygame.event.set_allowed(MOUSEBUTTONUP)

    running = True
    while running:
        if len(pygame.event.get()):
            break

        addWall(track, scale, screen, mouse.get_pos())

    pygame.event.set_allowed(None)

def updateScreen(rect = None):
    display.update(rect)
    pygame.event.get()
    clock.tick()

def uiRectangle(trackCoor, scale, size):
    screenPos = [(x*scale) - (x*scale) % scale for x in trackCoor]
    return Rect(screenPos[0], screenPos[1], scale*size, scale*size)

def blankTrack(scale, size):
    # Track
    track = RaceTrack((size - 3, size - 3), (2, 2), size)

    # Zones
    goal = Rect(scale, scale, scale * 3, scale * 3)
    start = Rect(size * scale - (4 * scale), size * scale - (4 * scale), scale * 3, scale * 3)

    # Open a window on the screen
    screen_width = size * scale
    screen_height = size * scale
    screen = pygame.display.set_mode([screen_width, screen_height])
    screen.fill(nullColor)

    # Draw the goal zone
    draw.rect(screen, startColor, start)
    draw.rect(screen, goalColor, goal)

    return track, screen

def main():
    pygame.init()
    scale = 5
    size = 100

    track, screen = blankTrack(scale, size)

    display.flip()

    running = True
    while running:
        clock.tick()
        # event handling, gets all event from the event queue
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                addWalls(track, scale, screen)

            if event.type == pygame.KEYDOWN:
                if event.__dict__['unicode'] == '\r':
                    addPath(track, scale, screen);
                if event.__dict__['unicode'] == '\b':
                    track, screen = blankTrack(scale, size);
                    display.flip();


            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False




if __name__== "__main__":
    # call the main function
    main()