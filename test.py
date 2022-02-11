"""
Random Walk Demonstration using Python Turtle Module
Compucademy - https://compucademy.net/
"""

import turtle
import random

BLOCK_SIZE = 60
BORDER = 13
STAMP_SIZE = 20  # Defualt value used to get pixel-level control of turtle size
ROWS = 8
COLUMNS = 10
SPEED = 10


def up():
    # Don't let walker off grid
    new_y = walker.ycor() - (BLOCK_SIZE + BORDER)
    if new_y >= -BORDER // 2:
        walker.sety(walker.ycor() - (BLOCK_SIZE + BORDER))
        return True  # Used to avoid counting moves which are disallowed


def down():
    new_y = walker.ycor() + (BLOCK_SIZE + BORDER)
    if new_y < screen.window_height():
        walker.sety(walker.ycor() + (BLOCK_SIZE + BORDER))
        return True


def left():
    new_x = walker.xcor() - (BLOCK_SIZE + BORDER)
    if new_x >= -BORDER // 2:
        walker.setx(walker.xcor() - (BLOCK_SIZE + BORDER))
        return True


def right():
    new_x = walker.xcor() + (BLOCK_SIZE + BORDER)
    if new_x < screen.window_width():
        walker.setx(walker.xcor() + (BLOCK_SIZE + BORDER))
        return True


def random_walk(num_steps):
    counter = 0
    directions = [up, down, left, right]
    while counter < num_steps:
        if random.choice(directions)():  # Call the chosen function and check the return value
            counter += 1


screen = turtle.Screen()
WIDTH = COLUMNS * (BLOCK_SIZE + BORDER)
HEIGHT = ROWS * (BLOCK_SIZE + BORDER)
screen.setup(WIDTH, HEIGHT)
screen.title("Random Walks Demo")
screen.setworldcoordinates(0, screen.window_height(), screen.window_width(), 0)
screen.bgcolor("black")
screen.tracer(0)  # Pause animation to get instant drawing

builder = turtle.Turtle(visible=False)
builder.shape("square")
builder.color("green")
builder.shapesize(BLOCK_SIZE / STAMP_SIZE)
builder.penup()

for row_num in range(ROWS):
    for col_num in range(COLUMNS):
        builder.goto((BLOCK_SIZE // 2) + col_num * (BLOCK_SIZE + BORDER),
                     (BLOCK_SIZE // 2) + row_num * (BLOCK_SIZE + BORDER))
        builder.stamp()

walker = turtle.Turtle()
walker.shape("circle")
walker.color("white")
walker.width(BORDER // 2)
walker.speed(SPEED)
walker.penup()
walker.goto(screen.window_width() // 2 - BORDER // 2, screen.window_height() // 2 - BORDER // 2)
walker.pendown()

screen.tracer(1)  # Restore animation
random_walk(15)
turtle.done()