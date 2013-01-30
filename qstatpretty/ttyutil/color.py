# -*- coding: utf8 -*-

COLOR_BLACK = 30
COLOR_RED = 31
COLOR_GREEN = 32
COLOR_YELLOW = 33
COLOR_BLUE = 34
COLOR_MAGENTA = 35
COLOR_CYAN = 36
COLOR_WHITE = 37


def colortext(t, color, bold=False):
    if not color:
        return t

    x = 1 if bold else 0
    return u"\033[{x};{y}m{text}\033[0m".format(x=x, y=color, text=t)
