import random, enum

class Coordinate:
    '''
    Implements a simple 2D x/y coordinate system.

    Used by shapes for positions, sizes, velocities etc.
    Supports simple arithmetical operations with scalars.
    '''

    def __init__(self, x=None, y=None):
        self.x = x if x is not None else random.randint(256)
        self.y = y if y is not None else random.randint(256)


    def __add__(self, other):
        if hasattr(other, "x") and hasattr(other, "y"):
            return Coordinate(self.x+other.x,
                              self.y+other.y)
        else:
            return Coordinate(self.x+other,
                              self.y+other)


    def __iadd__(self, other):
        if hasattr(other, "x") and hasattr(other, "y"):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self


    def __mul__(self, scalar):
        return Coordinate(self.x*scalar, self.y*scalar)

    
    def __imul__(self, scalar):
        self.x *= scalar
        self.y *= scalar
        return self


class Crossing(enum.IntEnum):
    '''
    Formalize crossing of boundaries
    '''
    Top    = 0
    Bottom = 1
    Left   = 2
    Right  = 3

    
class BoundingBox:
    '''
    Holding togetjer an "area".

    We have different posibilities of initialization,
    but we always reduce everything to the 
    '''
    top = 0
    left = 0
    bottom = 0
    right = 0

    def __init__(self, top=None, left=None, bottom=None, right=None
                 center=None, size=None):
        if center is not None:
            if size is None:
                raise RuntimeError(
                    "user either top/left/bottom/right, '
                    'or center/size"
                )
            self.top    = center.y-size.y/2
            self.bottom = center.y+size.y/2
            self.left   = center.x-size.x/2
            self.right  = center.x-size.x/2
        else:
            for margin in ("top", "left", "bottom", "right"):
                if locals()[margin] is None:
                    raise RuntimeError(f'{margin} is missing')
                setattr(self, margin, locals()[margin])


    def crosses(self, thing):
        '''
        Checks if "thing" is inside or outside (i.e. "crosses") the bounding box.

        Returns a tuple with the margins (see `Crossing`) where the crossing
        happens. If there's no crossing (i.e. the "thing" is inside), the
        tuple is empty -- see also .inside()).

        `thing` is expected to be a Coordinate.
        '''
        crs = []
        
        if thing.x < self.left:
            crs.append(Crossing.Left)
            
        if thing.x > self.right:
            crs.append(Crossing.Right)
            
        if thing.y < self.top:
            crs.append(Crossing.Top)

        if thing.y > self.bottom:
            crs.append(Crossing.Bottom)

        return tuple(crs)


    def inside(self, thing):
        '''
        Checks if "thing" is inside bounding box.
        '''
        return len(self.crosses(thing)) == 0

            
class Shape:
    '''
    Base class for "things" bouncing around on the screen.

    Implements only common operations for all shapes, e.g.:
    - a bounding box property
    - moving by a specified amount
    '''

    def __init__(self, bbox, color, velocity):
        # These are not intended for use by external objects
        # Only derrived classes should use these.
        self._bbox = bbox
        self._color = color
        self._vel = velocity
        

    def bbox(self):
        if self._bbox is None:
            raise RuntimeError("'Shape' needs to be subclassed")
        return self._bbox


    def moveby(self, delta):
        '''
        Moves the object by "delta".
        '''
        self._bbox.top    += delta.y
        self._bbox.bottom += delta.y
        self._bbox.left   += delta.x
        self._bbox.right  += delta.x


    def advance(self, time_delta):
        self.moveby(self._vel * time_delta)


class Artist:
    '''
    Abstract class to graphically represent a `Shape`.

    The idea is that we want to implement several graphical
    backends (Turtle, Pygame, PyQt, ...).
    Here we implement the graphical primitives we need.

    This is an abstract base class to demonstrate the API only.
    '''

    def set_color(self, r, g, b):
        '''
        Sets the foreground color (RGB values).
        '''
        raise RuntimeError('not implemented')


    def draw_circle(self, center, radius):
        '''
        Draw a prefectly round circle around a center point.
        '''
        raise RuntimeError('not implemented')

    
    def draw_rect(self, top_left=None, center=None, size=None):
        '''
        Draw a rect, either specifying its center, or its top-left corner,
        and its size.
        '''
        raise RuntimeError('not implemented')


class Ball(Shape):
    '''
    Represent a circular shape
    '''
    def __init__(self, center, radius, color=None, r=0, g=0, b=0):
        '''
        Args:
            center: middle of the circle
            radius: ...yep. It's the radius.
            color: an (R, G, B) tuple
        '''
        super().__init__()
        self._bbox = BoundingBox(center=center, size=Coordinate(radius*2, radius*2))
        self._color = color if color is not None else (r, g, b)


    def draw(self, artist):
        artist.set_color(*self._color)

        # reconstruct information from bbox
        center = Coordinate(
            self._bbox.left + (self._bbox.right-self._bbox.left)/2,
            self._bbox.top  + (self._bbox.bottom-self._bbox.top)/2,
        )
        radius = (self._bbox.right - self._bbox.left)/2

        artist.draw_circle(center, radius)
