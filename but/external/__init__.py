from ..lazy import LazyVariable
from .external_executable import (
    ExternalExecutable,
    ExternalExecutableDocker,
    ExternalExecutableNodeJS,
)
from .node_modules import find_node_modules, find_node_modules_binary

__all__ = ['Tools', 'find_node_modules', 'find_node_modules_binary']

PORTS = 'reireireireireireireireirei/ports:1.0.1'


class Tools:
    docker = LazyVariable(
        lambda: ExternalExecutable(
            executable='docker',
            version_option='--version',
            version_pattern=r'Docker version (.+?),',
        )
    )
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
    jpeg2png = LazyVariable(
        lambda: ExternalExecutableDocker(
            docker_image=PORTS,
            executable='/usr/local/bin/jpeg2png',
            version_option='--version',
            version_pattern=r'jpeg2png version (\S+)',
        )
    )

    def __new__(cls):
        raise TypeError(f'Cannot instantiate static class {cls.__name__}')
