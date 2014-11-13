from __future__ import print_function


def uname():
    from . import get_platform_string
    print(get_platform_string(), end='')


def git_version():
    from . import get_version_from_git
    print(get_version_from_git().lstrip('v.'), end='')


def git_short_version():
    from . import get_version_from_git, shorten_version_string
    print(shorten_version_string(get_version_from_git().lstrip('v.')), end='')
