

__PARSERS = {}


def parser(name):
    """Decorator to denote a parser for a certain grid system's output"""

    def inner(f):
        __PARSERS[name] = f
        return f

    return inner


def get_parser_by_name(name):
    return __PARSERS[name]


def get_parser_names():
    return __PARSERS.keys()


import qstatpretty.parser.gridengine
import qstatpretty.parser.torque
