from .. import VERSION

__all__ = ['init_cli', 'invoke_cli']


def init_cli(parent):
    _parser = parent.add_parser('version', add_help=False)

    return ['version']


def invoke_cli(args):
    match args.command:
        case 'version':
            print(f'Your Bunny Wrought version {VERSION}')


invoke_cli.naked = True
