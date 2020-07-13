def wrap_string(string: str, max_length: int):
    if len(string) <= max_length:
        return string

    if not string[max_length - 1].isspace():
        break_point = string[:max_length].rfind(' ') + 1
        first, second = string[:break_point], string[break_point:]
    else:
        first, second = string[:max_length], string[max_length:]

    if len(second) > max_length:
        return first + "\n" + wrap_string(second, max_length)
    else:
        return first + "\n" + second
