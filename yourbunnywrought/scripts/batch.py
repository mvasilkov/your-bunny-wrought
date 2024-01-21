from __future__ import annotations

from pathlib import Path
from shlex import split

from ..store import Store

__all__ = ['init_cli', 'invoke_cli', 'run', 'run_line', 'run_script']


class UnknownModuleError(RuntimeError):
    pass


def run(args, module):
    store = Store()
    store.set_burrow(args.burrow)
    store.working_directory = args.working_dir

    if module is not None:
        module.invoke_cli(args)


def run_line(tokens: list[str]):
    from ..args import get_args_module

    args, module = get_args_module(tokens)

    if module is None:
        raise UnknownModuleError()

    run(args, module)


def run_script(script: Path):
    for line in script.read_text(encoding='utf-8').splitlines():
        try:
            print(f'{script.name} │ {line}')
            run_line(split(line))
        except UnknownModuleError:
            print('Unknown operation')
            break
