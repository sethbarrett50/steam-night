from __future__ import annotations

import cs.demo as demo


class ErrorPen:
    def shape(self, value: str) -> None:
        pass

    def speed(self, value: int) -> None:
        pass

    def width(self, value: int) -> None:
        pass

    def undo(self) -> None:
        raise demo.turtle.TurtleGraphicsError('nothing to undo')

    def clear(self) -> None:
        pass

    def penup(self) -> None:
        pass

    def home(self) -> None:
        pass

    def pendown(self) -> None:
        pass


class FakeScreen:
    def __init__(self) -> None:
        self.handlers = {}

    def title(self, value: str) -> None:
        pass

    def setup(self, width: int, height: int) -> None:
        pass

    def bgcolor(self, value: str) -> None:
        pass

    def listen(self) -> None:
        pass

    def onkey(self, func, key: str) -> None:
        self.handlers[key] = func

    def bye(self) -> None:
        pass

    def mainloop(self) -> None:
        pass


def test_undo_handler_ignores_turtle_graphics_error(monkeypatch) -> None:
    fake_screen = FakeScreen()
    error_pen = ErrorPen()

    monkeypatch.setattr(demo.turtle, 'Screen', lambda: fake_screen)
    monkeypatch.setattr(demo.turtle, 'Turtle', lambda: error_pen)
    monkeypatch.setattr(demo, 'render_status', lambda state: None)

    demo.run_demo()

    fake_screen.handlers['u']()
