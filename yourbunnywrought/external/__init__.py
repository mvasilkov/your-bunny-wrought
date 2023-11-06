from enum import Enum

from ..lazy import LazyVariable
from .external_executable import ExternalExecutable

__all__ = ['ExternalExecutable', 'Tools']


class Tools(Enum):
    ffmpeg = LazyVariable(
        lambda: ExternalExecutable(
            executable='ffmpeg',
            version_option='-version',
            version_pattern=r'ffmpeg version (\S+)',
        )
    )
