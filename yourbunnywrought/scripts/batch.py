from __future__ import annotations

from pathlib import Path
from shlex import split
import sys
from typing import IO

from ..argtypes import ArgTypes
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


def run_line(tokens: list[str], replace_stdin: IO[str] | None = None):
    from ..args import get_args_module

    args, module = get_args_module(tokens)

    if module is None:
        raise UnknownModuleError()

    if replace_stdin is not None:
        for var in vars(args):
            if getattr(args, var) is sys.stdin:
                setattr(args, var, replace_stdin)

    run(args, module)


def run_script(script: IO[str] | Path):
    file_contents = script.read_text(encoding='utf-8') if isinstance(script, Path) else script.read()
    lines = file_contents.splitlines()

    for line in lines:
        tokens = split(line)

        try:
            print(f'{script.name} │ {line}')
            run_line(tokens)
        except UnknownModuleError:
            print('Unknown operation')
            break


def init_cli(parent):
    parser = parent.add_parser('run_script', aliases=['run'], add_help=False)

    parser.add_argument(
        'script_file',
        type=ArgTypes.one_of_type(
            ArgTypes.stdin_literal_type,
            ArgTypes.existing_script_file_type,
        ),
    )

    return ['run_script', 'run']


def invoke_cli(args):
    match args.command:
        case 'run_script' | 'run':
            run_script(args.script_file)
