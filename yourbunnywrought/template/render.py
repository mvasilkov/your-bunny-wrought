from __future__ import annotations

from functools import cache

from django.template import Context, Engine


@cache
def get_engine(dirs: list[str] | None) -> Engine:
    return Engine(dirs=dirs)


def render_to_string(template_str: str, context: dict, dirs: list[str] | None = None) -> str:
    template = get_engine(dirs).from_string(template_str)
    return template.render(Context(context))
