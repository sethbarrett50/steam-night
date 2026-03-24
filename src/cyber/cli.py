from __future__ import annotations

import argparse

from cyber.crack import crack_password
from cyber.server import DemoConfig, create_app


def run_server() -> None:
    parser = argparse.ArgumentParser(
        description="Run the Raspberry Pi cyber demo server."
    )
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--password", default="dragon")
    args = parser.parse_args()

    app = create_app(DemoConfig(password=args.password))
    app.run(host=args.host, port=args.port, debug=False)


def run_cracker() -> None:
    parser = argparse.ArgumentParser(
        description="Run the laptop-side dictionary attack demo."
    )
    parser.add_argument("--target", required=True)
    parser.add_argument("--delay", type=float, default=0.4)
    parser.add_argument("--wordlist", default=None)
    args = parser.parse_args()

    crack_password(
        target=args.target,
        delay=args.delay,
        wordlist_path=args.wordlist,
    )
