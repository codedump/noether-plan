#!/usr/bin/python3

import random
import pygame

# We use array() from the Numpy library because mathematical
# operations on array() are more efficient over list() operations
from numpy import array
    

class Ball:
    # several balls will be bouncing around the screen.
    # we start with 1 ball in this version
    
    # ball current position (pixels)
    pos = array([random.randint(300, 700), random.randint(300, 700)])

    # ball velocities in pixels/sec
    vel = array([random.randint(-500, 500), random.randint(-500, 500)])

    # ball size(s)
    rad = random.randint(15, 35)

    # ball colors
    rgb = array([128, 0, 0])


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
    ball = Ball()


#
# simple version: draw a single ball (index `i`)
# and update position of only a single ball
# (the one at index `i`)
#
def draw_ball_single(ball, screen):
    pygame.draw.circle(screen,
                       ball.rgb,
                       (ball.pos[0], ball.pos[1]),
                       ball.rad)


def move_ball_single(ball, t, bbox):
    ball.pos += (ball.vel*t).astype(int)
    
    if ((ball.pos[0]-ball.rad) <= bbox[0]) or ((ball.pos[0]+ball.rad) >= bbox[2]):
        ball.vel[0] *= -1

    if ((ball.pos[1]-ball.rad) <= bbox[1]) or ((ball.pos[1]+ball.rad) >= bbox[3]):
        ball.vel[1] *= -1

    # ACHTUNG: the upper two lines are very repetitive -- we
    # essentially write the same code for every direcion (vertical
    # and horizontal), and the only thing that changes is the index
    # of the position / velocity.
    #
    # Can you think of a way to simplify that, make it a single
    # line with a 'for' loop?



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
        
        move_ball_single(game.ball, game.period, (0, 0, size[0], size[1]))
        draw_ball_single(game.ball, screen)
    
        pygame.display.flip()
        clock.tick(1.0/game.period)

    pygame.quit()


# Run the main application
run_pygame()
