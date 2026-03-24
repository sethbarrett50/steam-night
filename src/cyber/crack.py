from __future__ import annotations

import time

from pathlib import Path

import requests

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

DEFAULT_WORDLIST = [
    "123456",
    "password",
    "qwerty",
    "letmein",
    "monkey",
    "dragon",
    "baseball",
    "sunshine",
]


def load_wordlist(path: str | None) -> list[str]:
    if path is None:
        return DEFAULT_WORDLIST

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Wordlist not found: {file_path}")

    words = [
        line.strip()
        for line in file_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not words:
        raise ValueError("Wordlist is empty.")
    return words


def crack_password(
    target: str,
    delay: float = 0.01,
    wordlist_path: str | None = None,
) -> str | None:
    console = Console()
    words = load_wordlist(wordlist_path)

    console.print(
        Panel.fit(
            "[bold cyan]Starting safe demo dictionary attack[/bold cyan]\n"
            "This is a classroom simulation.",
            title="Cyber Demo",
        )
    )

    attempts_table = Table(title="Password Attempts")
    attempts_table.add_column("Attempt #", justify="right")
    attempts_table.add_column("Password Tried")
    attempts_table.add_column("Result")

    for index, word in enumerate(words, start=1):
        try:
            response = requests.post(
                f"{target.rstrip('/')}/api/check",
                json={"password": word},
                timeout=5,
            )
            response.raise_for_status()
            success = bool(response.json().get("success", False))
        except requests.RequestException as exc:
            console.print(f"[bold red]Request failed:[/bold red] {exc}")
            return None

        result = "FOUND ✅" if success else "no match"
        attempts_table.add_row(str(index), word, result)

        console.clear()
        console.print(attempts_table)

        if success:
            console.print(
                Panel.fit(
                    f"[bold green]Password found:[/bold green] [yellow]{word}[/yellow]\n"
                    "Weak passwords are easy for computers to guess.",
                    title="Demo Result",
                )
            )
            return word

        time.sleep(delay)

    console.print(
        Panel.fit(
            "[bold red]Password not found in demo wordlist.[/bold red]",
            title="Demo Result",
        )
    )
    return None
