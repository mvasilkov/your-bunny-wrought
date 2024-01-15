from . import Tools

__all__ = ['init_cli', 'invoke_cli']


def init_cli(parent):
    parser = parent.add_parser('ffmpeg', aliases=['tsc'], add_help=False)

    parser.add_argument('options', nargs='*')

    return ['ffmpeg', 'tsc']


def invoke_cli(args):
    executable = getattr(Tools, args.command)

    result = executable.run(*args.options)

    print(result)
