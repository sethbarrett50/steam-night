from __future__ import annotations

import random

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    import turtle

COLORS = [
    'red',
    'orange',
    'gold',
    'green',
    'deepskyblue',
    'blue',
    'purple',
    'magenta',
]


def random_color() -> str:
    return random.choice(COLORS)


def square_spiral(pen: turtle.Turtle, size: int, repeats: int) -> str:
    for i in range(repeats):
        pen.pencolor(COLORS[i % len(COLORS)])
        pen.forward(size + i * 4)
        pen.right(90)
    return 'for i in range(repeats):\n    forward(size + i * 4)\n    right(90)'


def star_burst(pen: turtle.Turtle, size: int, repeats: int) -> str:
    for i in range(repeats):
        pen.pencolor(COLORS[i % len(COLORS)])
        pen.forward(size)
        pen.backward(size)
        pen.right(360 / repeats)
    return 'for i in range(repeats):\n    forward(size)\n    backward(size)\n    right(360 / repeats)'


def flower(pen: turtle.Turtle, size: int, repeats: int) -> str:
    for i in range(repeats):
        pen.pencolor(COLORS[i % len(COLORS)])
        pen.circle(size)
        pen.right(360 / repeats)
    return 'for i in range(repeats):\n    circle(size)\n    right(360 / repeats)'


def rainbow_polygons(pen: turtle.Turtle, size: int, repeats: int) -> str:
    sides = max(3, min(8, repeats // 2))
    for i in range(repeats):
        pen.pencolor(COLORS[i % len(COLORS)])
        for _ in range(sides):
            pen.forward(size + i * 2)
            pen.right(360 / sides)
        pen.right(15)
    return (
        'for i in range(repeats):\n'
        '    for _ in range(sides):\n'
        '        forward(size + i * 2)\n'
        '        right(360 / sides)\n'
        '    right(15)'
    )


PATTERNS: dict[str, tuple[str, Callable[[turtle.Turtle, int, int], str]]] = {
    '1': ('Square Spiral', square_spiral),
    '2': ('Star Burst', star_burst),
    '3': ('Flower', flower),
    '4': ('Rainbow Polygons', rainbow_polygons),
}
