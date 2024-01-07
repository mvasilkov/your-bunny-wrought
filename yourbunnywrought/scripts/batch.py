from shlex import split

from ..store import Store


def invoke(args, module):
    store = Store()
    store.set_burrow(args.burrow)
    store.working_directory = args.working_dir

    if module is not None:
        module.invoke_cli(args)


def invoke_line(line: str):
    from ..args import parser
    from ..cli_modules import CLI_RESOLVE_CMD_TO_MOD

    args = parser.parse_args(split(line))
    module = CLI_RESOLVE_CMD_TO_MOD.get(args.command)

    invoke(args, module)
