from pathlib import Path

from ..external.ansi import clean_ansi

FILES_DIR = Path(__file__).parent / 'files'


def test_clean_ansi():
    git_ansi = (FILES_DIR / 'git_ansi.txt').read_bytes()
    git_plain = (FILES_DIR / 'git_plain.txt').read_bytes()

    assert clean_ansi(git_ansi) == git_plain
