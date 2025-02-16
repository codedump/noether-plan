#!/usr/bin/python3

import random
from numpy import array

import pygame
    

class Balls:
    # several balls will be bouncing around the screen.
    # we start with 1, but we prepare for having a large
    # number.
    
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
# simple version: draw a single ball (index `i`)
# and update position of only a single ball
# (the one at index `i`)
#
def draw_ball_single(balls, screen, i=0):
    pygame.draw.circle(screen,
                       balls.rgb[i],
                       (balls.pos[i][0], balls.pos[i][1]),
                       balls.rad[i])

def move_ball_single(balls, t, bbox, i=0):
    balls.pos[i] += (balls.vel[i]*t).astype(int)
    
    if ((balls.pos[i,0]-balls.rad) <= bbox[0]) or ((balls.pos[i,0]+balls.rad) >= bbox[2]):
        balls.vel[i][0] *= -1

    if ((balls.pos[i,1]-balls.rad) <= bbox[1]) or ((balls.pos[i,1]+balls.rad) >= bbox[3]):
        balls.vel[i][1] *= -1


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
            ((balls.pos[:,coord_index]-balls.rad) <= bbox[coord_index]) or \
            ((balls.pos[:,coord_index]+balls.rad) >= bbox[coord_index+2])
        balls.vel[out_of_bounds,coord_index] *= -1


def draw_balls(balls, screen):
    '''
    Puts all balls on the screen.
    '''
    for pos,rad,col in zip(balls.pos, balls.rad, balls.rgb):
        pygame.draw.circle(screen, col, (pos[0], pos[1]), rad)

    
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
    
    while game.running:

        screen.fill((0,0,0))
             
        handle_events(game)
        
        move_ball_single(game.balls, game.period, (0, 0, size[0], size[1]))
        draw_ball_single(game.balls, screen)
    
        pygame.display.flip()
        clock.tick(1.0/game.period)

    pygame.quit()


# Run the main application
run_pygame()
