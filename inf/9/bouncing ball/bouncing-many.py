#!/usr/bin/python3

import random
import pygame

from numpy import array

# We need more array()-based operations: glueing arrays
# together ("concatenate") and calculating random numbers
# in arrays, all at once.
from numpy import concatenate
from numpy.random import rand as random_array
    

class Balls:
    # several balls will be bouncing around the screen.
    # we start with 1, but we prepare for having a large
    # number.

    #
    # Because we want to move many balls at once, each
    # information (position, velocity, radii, colors)
    # now need an extra dimention upfront.
    # Here, too, we are using array().
    #
    # We only initialize the game data with one single ball.
    # But below we define add_balls(), which can add a large
    # number of random balls to these data.
    #
    
    # balls current position (pixels)
    pos = array([[random.randint(300, 700),
                  random.randint(300, 700)]])

    # balls velocities in pixels/sec
    vel = array([[random.randint(-500, 500),
                  random.randint(-500, 500)]])

    # ball size(s)
    rad = array([random.randint(15, 35)])

    # ball colors
    rgb = array([(128, 0, 0)])


class GameData:
    '''
    Main structure to hold of the game's internal data.
    There is no graphical representation here, only data.
    '''
    
    # game ends when this is set to False
    running = True
    
    # time in seconds which one frame of the game takes
    period = 1.0/60.0

    # balls collection
    balls = Balls()


#
# performance version: handle multiple balls (all of them)
# use numpy array() to do calculations on all balls at
# the same time
#
def move_balls(balls, t, bbox):
    '''
    Advances balls each one time step ahead.
    If any balls reaches any of the edges, the velocities
    receive an inversed sign so the balls move the other way.

    Args:
        balls: collection of balls (the Balls object)
        t: time step
        bbox: bounding box within which to confige
          the balls
    '''
    
    balls.pos += (balls.vel*t).astype(int)

    for coord_index in range(2):
        out_of_bounds = \
            ((balls.pos[:,coord_index]-balls.rad) <= bbox[coord_index]) + \
            ((balls.pos[:,coord_index]+balls.rad) >= bbox[coord_index+2])
        balls.vel[out_of_bounds,coord_index] *= -1


def draw_balls(balls, screen):
    '''
    Puts all balls on the screen.
    '''
    for pos,rad,col in zip(balls.pos, balls.rad, balls.rgb):
        pygame.draw.circle(screen, col, (pos[0], pos[1]), rad)


def add_balls(balls, bbox=None, num=1):
    '''
    Creates more balls, adding them to the game data.
    Ball data (positions, coordinates, colors, velocities)
    are all random.

    Args:
        balls: the game's `Balls` structure
        bbox: bounding box within which to initialize
          the balls positions; if not specified, we default
          to a hard-coded rectangle.
        num: number of balls to add
    '''

    if bbox is None:
        bbox = (300, 300, 700, 700)

    upper_left  = array([bbox[0], bbox[1]])
    lower_right = array([bbox[2], bbox[3]])

    box_size = lower_right - upper_left
    
    new_pos = (upper_left + random_array(num, 2) * box_size).astype(int)
    new_vel = (      -500 + random_array(num, 2) * 1000).astype(int)
    new_rgb = (             random_array(num, 3) * 255).astype(int)
    new_rad = (        10 + random_array(num)    * 25).astype(int)
    
    balls.pos = concatenate((balls.pos, new_pos))
    balls.vel = concatenate((balls.vel, new_vel))
    balls.rgb = concatenate((balls.rgb, new_rgb))
    balls.rad = concatenate((balls.rad, new_rad))


def handle_events(g):
    '''
    Extracts events from the pygame event queue and updates
    the `GameData` structure in `g` to reflect the changes.
    This includes quitting the game, e.g. when the key "q"
    is pressed.
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            g.running = False
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_q):
            g.running = False


def run_pygame():
    '''
    The main application function.
    '''

    pygame.init()
    clock = pygame.time.Clock()

    # The game data
    game = GameData()

    # Display size in pixels
    size = (1280, 720)
    screen = pygame.display.set_mode(size)

    add_balls(game.balls, bbox=(50, 50, size[0]-50, size[1]-50), num=100)
    
    while game.running:

        screen.fill((0,0,0))
             
        handle_events(game)
        
        move_balls(game.balls, game.period, (0, 0, size[0], size[1]))
        draw_balls(game.balls, screen)
    
        pygame.display.flip()
        clock.tick(1.0/game.period)

    pygame.quit()


# Run the main application
run_pygame()
