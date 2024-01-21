from .external import cli as external
from .http import server
from .scripts import echo
from .template import render
from .watch import watch_files

__all__ = ['CLI_MODULES', 'CLI_RESOLVE_CMD_TO_MOD']

CLI_MODULES = [
    external,
    server,
    echo,
    render,
    watch_files,
]

CLI_RESOLVE_CMD_TO_MOD = {}  # Populated in args.py
