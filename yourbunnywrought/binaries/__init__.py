from pathlib import Path
import platform

from ..store import Store


def _get_platform():
    (system, _, _, _, machine, _) = platform.uname()
    if system == 'Darwin':
        (release, _, _) = platform.mac_ver()
        if release:
            system = 'macOS'
    return f'{system}_{machine}'.lower()


PLATFORM = _get_platform()
EXE = '.exe' if PLATFORM.startswith('win') else ''
PROGRAMS = Path(__file__).parent.resolve() / PLATFORM


def get_bundled_binary(name: str) -> Path | None:
    archive_path = PROGRAMS / (name + EXE + '.xz')
    if not archive_path.is_file():
        return None

    store = Store()

    bin_path = store.burrow / 'bin'
    if not bin_path.is_dir():
        bin_path.mkdir(parents=True)
