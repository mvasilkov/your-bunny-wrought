from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from enum import StrEnum
import json
from pathlib import Path
from struct import unpack

__all__ = ['init_cli', 'invoke_cli', 'align_int', 'load_asar', 'unpack_asar']


def align_int(n: int, p: int) -> int:
    '''
    Round the integer `n` up to the nearest multiple of `p` (a power of 2).
    '''
    return (n + p - 1) & -p


class AsarEntryType(StrEnum):
    OTHER = 'unk '
    DIR = 'dir '
    FILE = 'file'


@dataclass
class AsarEntry:
    type: AsarEntryType
    path: Path | None = None
    size: int | None = None
    offset: int | None = None


class AsarArchive:
    def __init__(self, fp):
        fp.seek(12)
        size = unpack('<I', fp.read(4))[0]
        header_str = fp.read(size).decode('utf-8')

        self.fp = fp
        self.header = json.loads(header_str)
        self.header_end = align_int(16 + size, 4)

    def entries(self, path: Path, obj=None):
        if obj is None:
            obj = self.header

        if (files := obj.get('files')) is not None:
            yield AsarEntry(AsarEntryType.DIR, path=path)
            for name, props in files.items():
                yield from self.entries(path / name, props)
        elif (size := obj.get('size')) is not None and (offset := obj.get('offset')) is not None:
            yield AsarEntry(AsarEntryType.FILE, path=path, size=size, offset=int(offset))
        else:
            yield AsarEntry(AsarEntryType.OTHER, path=path)

    def unpack(self, entry: AsarEntry):
        match entry.type:
            case AsarEntryType.DIR:
                entry.path.mkdir(parents=True)

            case AsarEntryType.FILE:
                self.fp.seek(self.header_end + entry.offset)
                with entry.path.open('wb') as fp:
                    fp.write(self.fp.read(entry.size))


@contextmanager
def load_asar(infile: Path):
    with infile.open('rb') as fp:
        yield AsarArchive(fp)


def unpack_asar(infile: Path, outpath: Path):
    parent_dir = outpath.parent

    with load_asar(infile) as archive:
        for entry in archive.entries(outpath):
            print(f'{entry.type} │ {entry.path.relative_to(parent_dir)}')
            archive.unpack(entry)
