__all__ = ['init_cli', 'invoke_cli']


def init_cli(parent):
    parser = parent.add_parser('echo', add_help=False)

    parser.add_argument('-n', action='store_true')
    parser.add_argument('text', nargs='+')

    return ['echo']


def invoke_cli(args):
    match args.command:
        case 'echo':
            print(' '.join(args.text), end='' if args.n else '\n')
