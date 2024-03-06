from ..lazy import LazyVariable
from .external_executable import ExternalExecutable, ExternalExecutableNodeJS
from .node_modules import find_node_modules, find_node_modules_binary

__all__ = ['Tools', 'find_node_modules', 'find_node_modules_binary']


class Tools:
    ffmpeg = LazyVariable(
        lambda: ExternalExecutable(
            executable='ffmpeg',
            version_option='-version',
            version_pattern=r'ffmpeg version (\S+)',
        )
    )
    tsc = LazyVariable(
        lambda: ExternalExecutableNodeJS(
            executable='tsc',
            version_option='--version',
            version_pattern=r'Version (\S+)',
        )
    )

    def __new__(cls):
        raise TypeError(f'Cannot instantiate static class {cls.__name__}')
