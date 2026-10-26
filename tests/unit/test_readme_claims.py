"""The README states how many CLI commands exist; the parser is the truth.

A count written in prose drifts the moment a command ships - the README said
"thirty CLI commands" while the parser registered 35, and nothing noticed.
This pins the figure to the parser so the next command has to update the
README, in the spirit of test_licence_claims.py, which pins the licence
claims to the files that carry them.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from echo_memory.cli.main import build_parser

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"


def registered_commands() -> set[str]:
    """The top level command names the CLI actually accepts."""
    parser = build_parser()
    subparsers = [
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    ]
    assert subparsers, "the CLI has no subparsers, so it has no commands"
    return set(subparsers[0].choices)


def readme_command_count() -> int:
    """The command count the README claims, in digits.

    The README has to state the count as a number for this to be checkable;
    if it goes back to spelling it out, the search fails and the test says
    so rather than quietly passing.
    """
    text = " ".join(README.read_text().split())
    match = re.search(r"(\d+)\s+CLI commands", text)
    assert match, "the README no longer states a CLI command count in digits"
    return int(match.group(1))


def test_the_readme_command_count_matches_the_parser():
    commands = registered_commands()
    assert readme_command_count() == len(commands), (
        f"the README claims {readme_command_count()} CLI commands, "
        f"the parser registers {len(commands)}"
    )
