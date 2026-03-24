from __future__ import annotations

from cs.demo import DemoState, render_status


def test_render_status_runs_without_error() -> None:
    state = DemoState(
        size=50,
        repeats=20,
        selected_key='1',
        last_code='for i in range(3):\n    print(i)',
    )
    render_status(state)
