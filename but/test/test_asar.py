from pytest import mark

from ..archive import align_int


@mark.parametrize('p', [2, 4, 8, 16, 32, 64])
def test_align_int(p: int):
    f = fp = 0
    for n in range(256):
        if n > fp:
            f += 1
            fp = f * p
        assert align_int(n, p) == fp
