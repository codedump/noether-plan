#!/usr/bin/python

import pygame, random, time

from ball import Scene, Ball, Coordinate, Artist

class PygameArtist(Artist):
    '''
    Implementation of `ball.Artist` that renders to a Pygame canvas.
    '''
    
    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()

        # Display size in pixels
        self.size = (1280, 720)
        self.screen = pygame.display.set_mode(self.size)

        self._current_color = (128, 128, 0)


    def get_canvas_size(self):
        return Coordinate(self.size[0], self.size[1])


    def begin(self):
        self.screen.fill((0,0,0))


    def end(self):
        pygame.display.flip()


    def set_color(self, r, g, b):
        '''
        Sets the foreground color (RGB values).
        '''
        self._current_color = (r, g, b)

 
    def draw_circle(self, center, radius):
        '''
        Draw a prefectly round circle around a center point.
        '''
        pygame.draw.circle(self.screen,
                           self._current_color,
                           (center.x, center.y),
                           radius)

    
    def draw_rect(self, top_left=None, center=None, size=None):
        '''
        Draw a rect, either specifying its center, or its top-left corner,
        and its size.
        '''
        raise RuntimeError('not implemented')

    

class PygameApplication:
    '''
    Main application model: a scene with lots of balls.

    Initializes a Pygame display and renders the balls.
    '''
    
    def __init__(self, num_balls=100):
        
        self.scene = Scene()
        self.artist = PygameArtist()
        
        for i in range(num_balls):
            shape_color = (
                random.randint(0,255),
                random.randint(0,255),
                random.randint(0,255)
            )

            shape_position = Coordinate(
                random.randint(0, self.artist.get_canvas_size().x),
                random.randint(0, self.artist.get_canvas_size().y)
            )
            
            self.scene.add(
                Ball(shape_position, random.randint(10, 30), shape_color)
            )


    def step(self):
        self.artist.begin()
        self.scene.display(self.artist)
        self.artist.end()

    
    def run(self, fps=60):
        '''
        Runs the application in an endless loop.
        '''

        period = 1.0/fps
        
        while True:
            t0 = time.time()
            self.step()

            # Calculate how long 
            consumed = (time.time()-t0)
            time.sleep(max(period-consumed, 0))


# Running the main application
if __name__ == "__main__":
    app = PygameApplication()
    app.run()
