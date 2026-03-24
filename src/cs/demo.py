from __future__ import annotations

import turtle

from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cs.patterns import PATTERNS


@dataclass
class DemoState:
    size: int = 40
    repeats: int = 18
    selected_key: str = '1'
    last_code: str = ''


console = Console()


def render_status(state: DemoState) -> None:
    name, _ = PATTERNS[state.selected_key]

    table = Table(title='CS Pattern Lab')
    table.add_column('Control')
    table.add_column('Action')
    table.add_row('1 / 2 / 3 / 4', 'Choose pattern')
    table.add_row('Up / Down', 'Change size')
    table.add_row('Left / Right', 'Change repeats')
    table.add_row('Space', 'Run selected pattern')
    table.add_row('U', 'Undo')
    table.add_row('C', 'Clear')
    table.add_row('Q', 'Quit')

    console.clear()
    console.print(table)
    console.print(
        Panel.fit(
            f'[bold cyan]Selected:[/bold cyan] {name}\n'
            f'[bold cyan]Size:[/bold cyan] {state.size}\n'
            f'[bold cyan]Repeats:[/bold cyan] {state.repeats}',
            title='Current Settings',
        )
    )

    if state.last_code:
        console.print(Panel(state.last_code, title='Code Preview', border_style='green'))


def run_demo() -> None:
    screen = turtle.Screen()
    screen.title('STEAM Night - CS Pattern Lab')
    screen.setup(width=1000, height=700)
    screen.bgcolor('white')

    pen = turtle.Turtle()
    pen.shape('turtle')
    pen.speed(0)
    pen.width(3)

    state = DemoState()
    render_status(state)

    def select_pattern(key: str) -> None:
        state.selected_key = key
        render_status(state)

    def increase_size() -> None:
        state.size += 10
        render_status(state)

    def decrease_size() -> None:
        state.size = max(10, state.size - 10)
        render_status(state)

    def increase_repeats() -> None:
        state.repeats += 2
        render_status(state)

    def decrease_repeats() -> None:
        state.repeats = max(4, state.repeats - 2)
        render_status(state)

    def clear_screen() -> None:
        pen.clear()
        pen.penup()
        pen.home()
        pen.pendown()
        render_status(state)

    def undo() -> None:
        try:
            pen.undo()
        except turtle.TurtleGraphicsError:
            pass

    def run_pattern() -> None:
        _, pattern_func = PATTERNS[state.selected_key]
        state.last_code = pattern_func(pen, state.size, state.repeats)
        render_status(state)

    screen.listen()
    screen.onkey(lambda: select_pattern('1'), '1')
    screen.onkey(lambda: select_pattern('2'), '2')
    screen.onkey(lambda: select_pattern('3'), '3')
    screen.onkey(lambda: select_pattern('4'), '4')
    screen.onkey(increase_size, 'Up')
    screen.onkey(decrease_size, 'Down')
    screen.onkey(decrease_repeats, 'Left')
    screen.onkey(increase_repeats, 'Right')
    screen.onkey(run_pattern, 'space')
    screen.onkey(clear_screen, 'c')
    screen.onkey(undo, 'u')
    screen.onkey(screen.bye, 'q')

    screen.mainloop()
