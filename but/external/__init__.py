from ..lazy import LazyVariable
from .external_executable import (
    ExternalExecutable,
    ExternalExecutableDocker,
    ExternalExecutableNodeJS,
)
from .node_modules import find_node_modules, find_node_modules_binary

__all__ = ['Tools', 'find_node_modules', 'find_node_modules_binary']

PORTS_IMAGE = 'reireireireireireireireirei/ports:1.0.1'
PORTS_IMAGE_AMD64 = PORTS_IMAGE + '-amd64'


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
    michikoid = LazyVariable(
        lambda: ExternalExecutableNodeJS(
            executable='michikoid',
            version_option='--version',
            version_pattern=r'Michikoid version (\S+)',
        )
    )
    rollup = LazyVariable(
        lambda: ExternalExecutableNodeJS(
            executable='rollup',
            version_option='--version',
            version_pattern=r'rollup v(\S+)',
        )
    )
    terser = LazyVariable(
        lambda: ExternalExecutableNodeJS(
            executable='terser',
            version_option='--version',
            version_pattern=r'terser (\S+)',
        )
    )
    tsc = LazyVariable(
        lambda: ExternalExecutableNodeJS(
            executable='tsc',
            version_option='--version',
            version_pattern=r'Version (\S+)',
        )
    )
    advzip = LazyVariable(
        lambda: ExternalExecutableDocker(
            docker_image=PORTS_IMAGE,
            executable='/usr/local/bin/advzip',
            version_option='--version',
            version_pattern=r'advancecomp v(\S+)',
        )
    )
    ect = LazyVariable(
        lambda: ExternalExecutableDocker(
            docker_image=PORTS_IMAGE,
            executable='/usr/local/bin/ect',
            version_option='-help',
            version_pattern=r'Efficient Compression Tool[\s\S]+?^Version (\S+)',
        )
    )
    jpeg2png = LazyVariable(
        lambda: ExternalExecutableDocker(
            docker_image=PORTS_IMAGE_AMD64,
            platform='linux/amd64',
            executable='/usr/local/bin/jpeg2png',
            version_option='--version',
            version_pattern=r'jpeg2png version (\S+)',
        )
    )

    def __new__(cls):
        raise TypeError(f'Cannot instantiate static class {cls.__name__}')
