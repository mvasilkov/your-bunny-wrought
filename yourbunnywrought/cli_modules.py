from .http import server
from .template import render

__all__ = ['CLI_MODULES', 'CLI_RESOLVE_CMD_TO_MOD']

CLI_MODULES = [
    server,
    render,
]

CLI_RESOLVE_CMD_TO_MOD = {}  # Populated in args.py
