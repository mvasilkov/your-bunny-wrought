from . import Tools

__all__ = ['init_cli', 'invoke_cli']

_props = [prop for prop in vars(Tools) if not prop.startswith('_')]


def init_cli(parent):
    parser = parent.add_parser(_props[0], aliases=_props[1:], add_help=False)

    parser.add_argument('options', nargs='*')

    return _props


def invoke_cli(args):
    executable = getattr(Tools, args.command)

    executable.run(*args.options)
