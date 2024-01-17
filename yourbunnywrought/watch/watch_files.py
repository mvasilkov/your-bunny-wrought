from __future__ import annotations

from pathlib import Path

from watchfiles import watch


def watch_files(paths: list[Path]):
    for changes in watch(*paths):
        for change in changes:
            print(change)
