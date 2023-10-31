from pathlib import Path
import platform


def _get_platform():
    (system, _, _, _, machine, _) = platform.uname()
    if system == 'Darwin':
        (release, _, _) = platform.mac_ver()
        if release:
            system = 'macOS'
    return f'{system}_{machine}'.lower()


PACKAGES = Path(__file__).parent.resolve()
PLATFORM = _get_platform()
