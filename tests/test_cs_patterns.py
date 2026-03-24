from __future__ import annotations

from cs.patterns import (
    PATTERNS,
    flower,
    rainbow_polygons,
    square_spiral,
    star_burst,
)


class FakePen:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def pencolor(self, color: str) -> None:
        self.calls.append(('pencolor', color))

    def forward(self, distance: int | float) -> None:
        self.calls.append(('forward', distance))

    def backward(self, distance: int | float) -> None:
        self.calls.append(('backward', distance))

    def right(self, angle: int | float) -> None:
        self.calls.append(('right', angle))

    def circle(self, radius: int | float) -> None:
        self.calls.append(('circle', radius))


def test_patterns_registry_contains_expected_keys() -> None:
    assert set(PATTERNS.keys()) == {'1', '2', '3', '4'}


def test_square_spiral_draws_expected_steps() -> None:
    pen = FakePen()

    code = square_spiral(pen, size=10, repeats=3)

    assert 'for i in range(repeats)' in code
    assert pen.calls == [
        ('pencolor', 'red'),
        ('forward', 10),
        ('right', 90),
        ('pencolor', 'orange'),
        ('forward', 14),
        ('right', 90),
        ('pencolor', 'gold'),
        ('forward', 18),
        ('right', 90),
    ]


def test_star_burst_draws_expected_steps() -> None:
    pen = FakePen()

    code = star_burst(pen, size=25, repeats=4)

    assert 'backward(size)' in code
    assert pen.calls == [
        ('pencolor', 'red'),
        ('forward', 25),
        ('backward', 25),
        ('right', 90.0),
        ('pencolor', 'orange'),
        ('forward', 25),
        ('backward', 25),
        ('right', 90.0),
        ('pencolor', 'gold'),
        ('forward', 25),
        ('backward', 25),
        ('right', 90.0),
        ('pencolor', 'green'),
        ('forward', 25),
        ('backward', 25),
        ('right', 90.0),
    ]


def test_flower_draws_expected_steps() -> None:
    pen = FakePen()

    code = flower(pen, size=30, repeats=4)

    assert 'circle(size)' in code
    assert pen.calls == [
        ('pencolor', 'red'),
        ('circle', 30),
        ('right', 90.0),
        ('pencolor', 'orange'),
        ('circle', 30),
        ('right', 90.0),
        ('pencolor', 'gold'),
        ('circle', 30),
        ('right', 90.0),
        ('pencolor', 'green'),
        ('circle', 30),
        ('right', 90.0),
    ]


def test_rainbow_polygons_uses_minimum_three_sides() -> None:
    pen = FakePen()

    code = rainbow_polygons(pen, size=20, repeats=4)

    assert 'for _ in range(sides)' in code

    forward_calls = [call for call in pen.calls if call[0] == 'forward']
    right_calls = [call for call in pen.calls if call[0] == 'right']

    assert len(forward_calls) == 12  # 4 repeats * 3 sides
    assert right_calls.count(('right', 120.0)) == 12
    assert right_calls.count(('right', 15)) == 4


def test_rainbow_polygons_caps_sides_at_eight() -> None:
    pen = FakePen()

    rainbow_polygons(pen, size=20, repeats=20)

    forward_calls = [call for call in pen.calls if call[0] == 'forward']
    polygon_turns = [call for call in pen.calls if call == ('right', 45.0)]
    outer_turns = [call for call in pen.calls if call == ('right', 15)]

    assert len(forward_calls) == 160  # 20 repeats * 8 sides
    assert len(polygon_turns) == 160
    assert len(outer_turns) == 20
