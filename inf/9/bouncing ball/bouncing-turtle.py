#!/usr/bin/python3

import turtle as t
from random import random

screen = t.Screen()
screen.setup(1280, 720)

def make_ball(screen, pos=(0,0), color=None):
    display_ball = t.RawTurtle(screen)
    display_ball.hideturtle()    
    display_ball.speed(0)
    display_ball.penup()    
    display_ball.goto(pos)
    display_ball.pendown()
    if color is not None:
        display_ball.fillcolor(color)
    display_ball.begin_fill()
    display_ball.circle(27)
    display_ball.end_fill()
    display_ball.penup()

    return display_ball

b1 = make_ball(screen, pos=( 100,  100), color="red")
b2 = make_ball(screen, pos=(-100, -100))
b3 = make_ball(screen, pos=(-100,  100), color="green")
b4 = make_ball(screen, pos=( 100, -100), color="blue")

while True:
    screen.update()
    #b1.setx(b1.xcor()+1)
    b1.goto(50, 50)

screen.mainloop()
