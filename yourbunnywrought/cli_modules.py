from .http import server

__all__ = ['CLI_MODULES', 'CLI_RESOLVE_CMD_TO_MOD']

CLI_MODULES = [
    server,
]

CLI_RESOLVE_CMD_TO_MOD = {}  # Populated in args.py
