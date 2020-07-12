class _Getchar:
    """Gets a single character from standard input.  Does not echo to the screen."""

    def __init__(self):
        self.impl = _GetcharUnix()

    def __call__(self):
        return self.impl()


class _GetcharUnix:
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def getchar():
    _Getchar()()


def wrap_string(string: str, max_length: int):
    if len(string) <= max_length:
        return string

    if not string[max_length - 1].isspace():
        break_point = string[:max_length].rfind(' ')
        first, second = string[:break_point + 1], string[break_point + 1:]
    else:
        first, second = string[:max_length], string[max_length:]

    if len(second) > max_length:
        return first + "\n" + Helper.wrap_string(second, max_length)
    else:
        return first + "\n" + second
