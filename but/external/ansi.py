from io import BytesIO


# https://github.com/kilobyte/colorized-logs/blob/master/ansi2txt.c
def clean_ansi(in_bytes: bytes) -> bytes:
    'Port of ansi2txt.c'

    in_buf = BytesIO(in_bytes)
    out_buf = BytesIO()

    def getchar() -> bytes:
        return in_buf.read(1)

    def putchar(b: bytes):
        out_buf.write(b)

    while (ch := getchar()) != b'':
        while ch == b'\r':
            if (ch := getchar()) != b'\n':
                putchar(b'\r')  # suppress \r only when followed by \n
        if ch == b'\x1b':
            if (ch := getchar()) == b'[':
                while (ch := getchar()) == b';' or (ch >= b'0' and ch <= b'9') or ch == b'?':
                    pass
            elif ch == b']' and (ch := getchar()) >= b'0' and ch <= b'9':
                while True:
                    if (ch := getchar()) == b'' or ch == b'\x07':
                        break
                    elif ch == b'\x1b':
                        ch = getchar()
                        break
            elif ch == b'%' or ch == b'(' or ch == b')':
                ch = getchar()
        elif ch != b'':
            putchar(ch)

    return out_buf.getvalue()
