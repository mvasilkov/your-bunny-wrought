from __future__ import annotations

from functools import cache
from pathlib import Path
from typing import Iterable

from django.template import Context, Engine

from ..store import Store

__all__ = ['init_cli', 'invoke_cli', 'render_to_string']


@cache
def get_engine(dirs: tuple[str] | None) -> Engine:
    return Engine(dirs=dirs)


def render_to_string(template_str: str, context: dict, dirs: Iterable[str] | None = None) -> str:
    template = get_engine(tuple(dirs)).from_string(template_str)
    return template.render(Context(context))


def render_template(infile: Path, context: dict, dirs: Iterable[str] | None = None):
    if dirs is not None:
        dirs = tuple(dirs)

    outfile = infile.with_name(infile.name[1:])
    outfile.write_text(
        render_to_string(infile.read_text(encoding='utf-8'), context, dirs),
        encoding='utf-8',
        newline='\n',
    )


def init_cli(parent, ArgTypes):
    parser = parent.add_parser('render_template', aliases=['template'], add_help=False)

    parser.add_argument(
        '-t',
        '--template-dir',
        type=ArgTypes.existing_path_type,
        action='append',
    )
    parser.add_argument('pattern', nargs='+')

    return ['render_template', 'template']


def invoke_cli(args):
    store = Store()

    match args.command:
        case 'render_template' | 'template':
            for pattern in args.pattern:
                for path in store.working_directory.glob(pattern):
                    print('*', path.relative_to(store.working_directory))
                    render_template(path, {}, args.template_dir)
