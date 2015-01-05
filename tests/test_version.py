from os import path
from infi.os_info import get_version_from_git, get_version_from_file, shorten_version_string


def test_git():
    shorten_version_string(get_version_from_git())


def test_file():
    filepath = path.join('src', 'infi', 'os_info', '__version__.py')
    shorten_version_string(get_version_from_file(filepath))


def test_shortening():
    assert shorten_version_string("1.2.3") == "1.2.3"
    assert shorten_version_string("1.2.3.post1.g1234567") == "1.2.3.1"
    assert shorten_version_string("1.2.3.post1+g1234567") == "1.2.3.1"
    assert shorten_version_string("1.2.2.post1+g1234567") == "1.2.2.1"
