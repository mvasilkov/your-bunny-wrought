from __future__ import annotations

from functools import cache, cached_property
from pathlib import Path
import re
from shutil import which
from subprocess import CalledProcessError, check_call, check_output

from ..binaries import PLATFORM
from ..store import Store
from .node_modules import find_node_modules_binary

__all__ = [
    'ExternalExecutable',
    'ExternalExecutableNodeJS',
    'ExternalExecutableDocker',
]

NODEJS_EXT = '.cmd' if PLATFORM.startswith('win') else ''

which = cache(which)


class ExternalExecutable:
    def __init__(self, *, executable: str, version_option: str, version_pattern: str):
        self.executable = executable
        self.version_option = version_option
        self.version_pattern = version_pattern
        self.version_string = self.check_available()

    @cached_property
    def executable_path(self) -> list[str] | None:
        if (path := which(self.executable)) is not None:
            return [path]

    def check_available(self) -> str:
        if self.executable_path is None:
            raise RuntimeError(f'Cannot resolve {self.executable}')

        result = check_output([*self.executable_path, self.version_option], encoding='utf-8')

        version = re.match(self.version_pattern, result, re.MULTILINE)
        if version is None:
            raise RuntimeError(f'Cannot understand `{self.executable} {self.version_option}`, got {result!r}')

        return version.group(1)

    def run(self, *args):
        check_call([*self.executable_path, *args])

    def run_read_output(self, *args) -> str:
        return check_output([*self.executable_path, *args], encoding='utf-8')


class ExternalExecutableNodeJS(ExternalExecutable):
    def __init__(self, *, executable: str, version_option: str, version_pattern: str):
        super().__init__(
            executable=executable + NODEJS_EXT,
            version_option=version_option,
            version_pattern=version_pattern,
        )

    @cached_property
    def executable_path(self) -> list[Path | str] | None:
        if (path := find_node_modules_binary(self.executable)) is not None:
            return [path]

        if (path := which(self.executable)) is not None:
            return [path]


class ExternalExecutableDocker(ExternalExecutable):
    def __init__(
        self,
        *,
        docker_image: str,
        executable: str,
        version_option: str,
        version_pattern: str,
        platform: str | None = None,
    ):
        self.docker_image = docker_image
        self.platform = platform
        super().__init__(
            executable=executable,
            version_option=version_option,
            version_pattern=version_pattern,
        )

    @cached_property
    def docker_platform(self) -> str | None:
        if self.platform is not None:
            return self.platform

        if (path := which('docker')) is not None:
            try:
                platform = check_output([path, 'info', '-f', '{{.OSType}}/{{.Architecture}}'], encoding='utf-8')
                return platform.rstrip()
            except CalledProcessError:
                pass

    @cached_property
    def executable_path(self) -> list[str] | None:
        if (path := which('docker')) is not None:
            platform = ['--platform', self.docker_platform] if self.docker_platform is not None else []
            return [path, 'run', *platform, '--rm', self.docker_image, self.executable]

    @property
    def executable_path_mount(self) -> list[str] | None:
        if (path := self.executable_path) is not None:
            store = Store()

            working_dir = store.working_directory
            top_level_dir = Path('~').expanduser()
            if not working_dir.is_relative_to(top_level_dir):
                return path

            (path := path[:])[-2:-2] = ['-v', f'{top_level_dir}:{top_level_dir}', '-w', working_dir]
            return path

    def run(self, *args):
        check_call([*self.executable_path_mount, *args])

    def run_read_output(self, *args) -> str:
        return check_output([*self.executable_path_mount, *args], encoding='utf-8')
