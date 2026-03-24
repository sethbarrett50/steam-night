from __future__ import annotations

from cs import cli


def test_main_calls_run_demo(monkeypatch) -> None:
    called = {'value': False}

    def fake_run_demo() -> None:
        called['value'] = True

    monkeypatch.setattr(cli, 'run_demo', fake_run_demo)

    cli.main()

    assert called['value'] is True
