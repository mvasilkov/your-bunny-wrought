__all__ = ['Asar', 'align_int']


def align_int(n: int, p: int) -> int:
    '''
    Round the integer `n` up to the nearest multiple of `p` (a power of 2).
    '''
    return (n + p - 1) & -p


class Asar:
    pass
