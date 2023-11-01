from pathlib import Path
import platform


def _get_platform():
    (system, _, _, _, machine, _) = platform.uname()
    if system == 'Darwin':
        (release, _, _) = platform.mac_ver()
        if release:
            system = 'macOS'
    return f'{system}_{machine}'.lower()


PLATFORM = _get_platform()
EXE = '.exe' if PLATFORM.startswith('windows') else ''
PROGRAMS = Path(__file__).parent.resolve() / PLATFORM


def get_bundled_binary(name: str) -> Path | None:
    archive_path = PROGRAMS / (name + EXE + '.xz')
    if not archive_path.is_file():
        return None
