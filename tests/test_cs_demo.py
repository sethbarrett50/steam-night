from __future__ import annotations

from typing import Callable

import cs.demo as demo


class FakeScreen:
    def __init__(self) -> None:
        self.handlers: dict[str, Callable[[], None]] = {}
        self.title_value: str | None = None
        self.setup_args: tuple[int, int] | None = None
        self.bgcolor_value: str | None = None
        self.listen_called = False
        self.mainloop_called = False
        self.bye_called = False

    def title(self, value: str) -> None:
        self.title_value = value

    def setup(self, width: int, height: int) -> None:
        self.setup_args = (width, height)

    def bgcolor(self, value: str) -> None:
        self.bgcolor_value = value

    def listen(self) -> None:
        self.listen_called = True

    def onkey(self, func: Callable[[], None], key: str) -> None:
        self.handlers[key] = func

    def bye(self) -> None:
        self.bye_called = True

    def mainloop(self) -> None:
        self.mainloop_called = True


class FakePen:
    def __init__(self) -> None:
        self.shape_value: str | None = None
        self.speed_value: int | None = None
        self.width_value: int | None = None
        self.clear_called = False
        self.penup_called = False
        self.home_called = False
        self.pendown_called = False
        self.undo_called = False

    def shape(self, value: str) -> None:
        self.shape_value = value

    def speed(self, value: int) -> None:
        self.speed_value = value

    def width(self, value: int) -> None:
        self.width_value = value

    def clear(self) -> None:
        self.clear_called = True

    def penup(self) -> None:
        self.penup_called = True

    def home(self) -> None:
        self.home_called = True

    def pendown(self) -> None:
        self.pendown_called = True

    def undo(self) -> None:
        self.undo_called = True


def test_run_demo_initializes_screen_and_pen(monkeypatch) -> None:
    fake_screen = FakeScreen()
    fake_pen = FakePen()
    states: list[demo.DemoState] = []

    monkeypatch.setattr(demo.turtle, 'Screen', lambda: fake_screen)
    monkeypatch.setattr(demo.turtle, 'Turtle', lambda: fake_pen)
    monkeypatch.setattr(
        demo,
        'render_status',
        lambda state: states.append(
            demo.DemoState(
                size=state.size,
                repeats=state.repeats,
                selected_key=state.selected_key,
                last_code=state.last_code,
            )
        ),
    )

    demo.run_demo()

    assert fake_screen.title_value == 'STEAM Night - CS Pattern Lab'
    assert fake_screen.setup_args == (1000, 700)
    assert fake_screen.bgcolor_value == 'white'
    assert fake_screen.listen_called is True
    assert fake_screen.mainloop_called is True

    assert fake_pen.shape_value == 'turtle'
    assert fake_pen.speed_value == 0
    assert fake_pen.width_value == 3

    assert len(states) >= 1
    assert states[0].size == 40
    assert states[0].repeats == 18
    assert states[0].selected_key == '1'
    assert states[0].last_code == ''


def test_run_demo_registers_expected_keys(monkeypatch) -> None:
    fake_screen = FakeScreen()
    fake_pen = FakePen()

    monkeypatch.setattr(demo.turtle, 'Screen', lambda: fake_screen)
    monkeypatch.setattr(demo.turtle, 'Turtle', lambda: fake_pen)
    monkeypatch.setattr(demo, 'render_status', lambda state: None)

    demo.run_demo()

    expected_keys = {
        '1',
        '2',
        '3',
        '4',
        'Up',
        'Down',
        'Left',
        'Right',
        'space',
        'c',
        'u',
        'q',
    }
    assert set(fake_screen.handlers.keys()) == expected_keys


def test_key_handlers_update_state_and_call_pattern(monkeypatch) -> None:
    fake_screen = FakeScreen()
    fake_pen = FakePen()
    states: list[demo.DemoState] = []

    def fake_render_status(state: demo.DemoState) -> None:
        states.append(
            demo.DemoState(
                size=state.size,
                repeats=state.repeats,
                selected_key=state.selected_key,
                last_code=state.last_code,
            )
        )

    monkeypatch.setattr(demo.turtle, 'Screen', lambda: fake_screen)
    monkeypatch.setattr(demo.turtle, 'Turtle', lambda: fake_pen)
    monkeypatch.setattr(demo, 'render_status', fake_render_status)

    def fake_pattern(pen: object, size: int, repeats: int) -> str:
        assert pen is fake_pen
        return f'pattern size={size} repeats={repeats}'

    monkeypatch.setitem(demo.PATTERNS, '2', ('Test Pattern', fake_pattern))

    demo.run_demo()

    fake_screen.handlers['2']()
    assert states[-1].selected_key == '2'

    fake_screen.handlers['Up']()
    assert states[-1].size == 50

    fake_screen.handlers['Right']()
    assert states[-1].repeats == 20

    fake_screen.handlers['space']()
    assert states[-1].last_code == 'pattern size=50 repeats=20'


def test_down_and_left_respect_minimums(monkeypatch) -> None:
    fake_screen = FakeScreen()
    fake_pen = FakePen()
    states: list[demo.DemoState] = []

    monkeypatch.setattr(demo.turtle, 'Screen', lambda: fake_screen)
    monkeypatch.setattr(demo.turtle, 'Turtle', lambda: fake_pen)
    monkeypatch.setattr(
        demo,
        'render_status',
        lambda state: states.append(
            demo.DemoState(
                size=state.size,
                repeats=state.repeats,
                selected_key=state.selected_key,
                last_code=state.last_code,
            )
        ),
    )

    demo.run_demo()

    for _ in range(10):
        fake_screen.handlers['Down']()

    for _ in range(20):
        fake_screen.handlers['Left']()

    assert states[-1].size >= 10
    assert states[-1].repeats >= 4
    assert states[-1].size == 10
    assert states[-1].repeats == 4


def test_clear_handler_resets_pen_position(monkeypatch) -> None:
    fake_screen = FakeScreen()
    fake_pen = FakePen()

    monkeypatch.setattr(demo.turtle, 'Screen', lambda: fake_screen)
    monkeypatch.setattr(demo.turtle, 'Turtle', lambda: fake_pen)
    monkeypatch.setattr(demo, 'render_status', lambda state: None)

    demo.run_demo()

    fake_screen.handlers['c']()

    assert fake_pen.clear_called is True
    assert fake_pen.penup_called is True
    assert fake_pen.home_called is True
    assert fake_pen.pendown_called is True


def test_undo_handler_calls_pen_undo(monkeypatch) -> None:
    fake_screen = FakeScreen()
    fake_pen = FakePen()

    monkeypatch.setattr(demo.turtle, 'Screen', lambda: fake_screen)
    monkeypatch.setattr(demo.turtle, 'Turtle', lambda: fake_pen)
    monkeypatch.setattr(demo, 'render_status', lambda state: None)

    demo.run_demo()

    fake_screen.handlers['u']()

    assert fake_pen.undo_called is True


def test_q_handler_calls_screen_bye(monkeypatch) -> None:
    fake_screen = FakeScreen()
    fake_pen = FakePen()

    monkeypatch.setattr(demo.turtle, 'Screen', lambda: fake_screen)
    monkeypatch.setattr(demo.turtle, 'Turtle', lambda: fake_pen)
    monkeypatch.setattr(demo, 'render_status', lambda state: None)

    demo.run_demo()

    fake_screen.handlers['q']()

    assert fake_screen.bye_called is True
