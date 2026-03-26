from __future__ import annotations

import json
import time

from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

DEFAULT_WORDLIST = [
    '123456',
    'password',
    'qwerty',
    'letmein',
    'monkey',
    'dragon',
    'baseball',
    'sunshine',
]


def load_wordlist(path: str | None) -> list[str]:
    if path is None:
        return DEFAULT_WORDLIST

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f'Wordlist not found: {file_path}')

    words = [line.strip() for line in file_path.read_text(encoding='utf-8').splitlines() if line.strip()]
    if not words:
        raise ValueError('Wordlist is empty.')
    return words


def _check_password(
    target: str,
    password: str,
    timeout: float = 5.0,
) -> bool:
    url = f'{target.rstrip("/")}/api/check'
    payload = json.dumps({'password': password}).encode('utf-8')

    request = Request(
        url=url,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    with urlopen(request, timeout=timeout) as response:
        body = response.read().decode('utf-8')
        data = json.loads(body)
        return bool(data.get('success', False))


def crack_password(
    target: str,
    delay: float = 0.01,
    wordlist_path: str | None = None,
) -> str | None:
    console = Console()
    words = load_wordlist(wordlist_path)

    console.print(
        Panel.fit(
            '[bold cyan]🚀 Starting safe demo dictionary attack[/bold cyan]\n'
            'This is a classroom simulation on your local network.',
            title='Cyber Demo',
        )
    )

    attempts_table = Table(title='🔐 Password Attempts')
    attempts_table.add_column('Attempt #', justify='right')
    attempts_table.add_column('Password Tried')
    attempts_table.add_column('Result')

    for index, word in enumerate(words, start=1):
        try:
            success = _check_password(
                target=target,
                password=word,
                timeout=5.0,
            )
        except HTTPError as exc:
            console.print(f'[bold red]HTTP request failed:[/bold red] {exc.code} {exc.reason}')
            return None
        except URLError as exc:
            console.print(f'[bold red]Connection failed:[/bold red] {exc.reason}')
            return None
        except TimeoutError:
            console.print('[bold red]Connection timed out.[/bold red]')
            return None
        except json.JSONDecodeError:
            console.print('[bold red]Server returned invalid JSON.[/bold red]')
            return None

        result = 'FOUND ✅' if success else 'no match'
        attempts_table.add_row(str(index), word, result)

        console.clear()
        console.print(attempts_table)

        if success:
            console.print(
                Panel.fit(
                    f'[bold green]🎉 Password found:[/bold green] '
                    f'[yellow]{word}[/yellow]\n'
                    'Weak passwords are easy for computers to guess.',
                    title='Demo Result',
                )
            )
            return word

        time.sleep(max(delay, 0.0))

    console.print(
        Panel.fit(
            '[bold red]❌ Password not found in demo wordlist.[/bold red]',
            title='Demo Result',
        )
    )
    return None
