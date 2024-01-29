from __future__ import annotations

from dataclasses import dataclass
from functools import cache, cached_property
from os.path import isabs
from pathlib import Path
from typing import Iterable

from django.template import Context, Engine

from ..argtypes import ArgTypes
from ..html.parser import get_title
from ..store import Store

__all__ = ['init_cli', 'invoke_cli', 'render_to_string']


@dataclass(frozen=True)
class PageProps:
    title: str | None
    path: Path

    @cached_property
    def relative_path(self) -> str:
        store = Store()
        return self.path.relative_to(store.working_directory).as_posix()


@cache
def get_engine(dirs: tuple[str] | None) -> Engine:
    return Engine(dirs=dirs)


def render_to_string(template_str: str, context: dict, dirs: Iterable[str] | None = None) -> str:
    if dirs is not None:
        dirs = tuple(dirs)

    template = get_engine(dirs).from_string(template_str)
    return template.render(Context(context))


def render_template(
    infile: Path, context: dict, dirs: Iterable[str] | None = None, return_props=False
) -> PageProps | None:
    if dirs is not None:
        dirs = tuple(dirs)

    outfile = infile.with_name(infile.name[1:])
    outfile.write_text(
        hypertext := render_to_string(infile.read_text(encoding='utf-8'), context, dirs),
        encoding='utf-8',
        newline='\n',
    )

    if return_props:
        return PageProps(title=get_title(hypertext), path=outfile)


def init_cli(parent):
    parser = parent.add_parser('render_template', aliases=['template'], add_help=False)

    parser.add_argument(
        '-t',
        '--template-dir',
        type=ArgTypes.existing_directory_type,
        action='append',
    )
    parser.add_argument('-p', '--pages', action='store_true')
    parser.add_argument('pattern', nargs='+')

    return ['render_template', 'template']


def invoke_cli(args):
    store = Store()
    pages: list[PageProps] = []

    match args.command:
        case 'render_template' | 'template':
            for pattern in args.pattern:
                for path in _glob(store.working_directory, pattern):
                    print('*', path.relative_to(store.working_directory))
                    context = {'pages': pages} if args.pages else {}
                    page_props = render_template(path, context, args.template_dir, args.pages)
                    if page_props is not None:
                        pages.append(page_props)


def _glob(path: Path, pattern: str) -> Iterable[Path]:
    if isabs(pattern):
        return (Path(pattern),)

    return path.glob(pattern)
