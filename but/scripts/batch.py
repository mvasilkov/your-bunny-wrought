from __future__ import annotations

from io import StringIO
from pathlib import Path
from shlex import split
import subprocess
import sys
from threading import Thread
from typing import IO

from ..argtypes import ArgTypes
from ..store import Store

__all__ = ['init_cli', 'invoke_cli', 'run', 'run_line', 'run_script']


class UnknownModuleError(RuntimeError):
    pass


def run(args, module) -> Thread | None:
    store = Store()
    store.set_burrow(args.burrow)
    store.working_directory = args.working_dir

    if module is not None:
        if args.persistent or getattr(module.invoke_cli, 'persistent', False):
            thread = Thread(target=module.invoke_cli, args=(args,))
            thread.start()

            return thread

        module.invoke_cli(args)


def run_line(tokens: list[str], replace_stdin: IO[str] | None = None) -> Thread | None:
    from ..args import get_args_module

    args, module = get_args_module(tokens)

    if module is None:
        raise UnknownModuleError()

    if replace_stdin is not None:
        for var in vars(args):
            if getattr(args, var) is sys.stdin:
                setattr(args, var, replace_stdin)

    return run(args, module)


def run_script(script: IO[str] | Path):
    file_contents = script.read_text(encoding='utf-8') if isinstance(script, Path) else script.read()
    lines = (ln for ln in file_contents.splitlines())
    threads: list[Thread] = []

    for line in lines:
        if not line or line.startswith('#'):
            continue

        tokens = split(line)

        if tokens[-1].startswith('<<'):
            end = tokens.pop()[2:]

            collect_lines = []
            for ln in lines:
                if ln == end:
                    break
                collect_lines.append(ln)

            replace_stdin = StringIO('\n'.join(collect_lines))
        else:
            replace_stdin = None

        try:
            print(f'{script.name} │ {line}')
            if (thread := run_line(tokens, replace_stdin)) is not None:
                threads.append(thread)
        except UnknownModuleError:
            print('Unknown operation')
            break

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        sys.exit()


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
            if isinstance(args.script_file, Path) and args.script_file.suffix == '.py':
                subprocess.run([sys.executable, args.script_file])
                return

            run_script(args.script_file)
