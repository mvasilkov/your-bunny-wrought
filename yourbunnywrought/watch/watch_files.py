from __future__ import annotations

import asyncio
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

from watchfiles import Change, awatch

__all__ = ['watch_files']


@dataclass
class FileChangeHandler:
    patterns: list[str]
    script: list[str]
    expects_file: bool = False

    def __post_init__(self):
        self.expects_file = any(token == ':file' for token in self.script)

    def script_for_path(self, path: str):
        if not self.expects_file:
            return self.script

        return [token if token != ':file' else path for token in self.script]


_updates = asyncio.Queue()


async def watch_files(paths: list[Path], handlers: list[FileChangeHandler]):
    async for changes in awatch(*paths):
        for change, path in changes:
            for handler in handlers:
                if change is Change.deleted and handler.expects_file:
                    continue

                if not any(fnmatch(path, p) for p in handler.patterns):
                    continue

                _updates.put_nowait(handler.script_for_path(path))
                break
