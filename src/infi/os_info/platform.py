# Module with same api as built-in platform but different implementation of linux_distribution that uses distro's one.
from __future__ import absolute_import
from platform import *


def linux_distribution():
    """
    Return information about the current OS distribution as a tuple:
    (name, version, codename)
    """
    import distro
    name, version, codename = distro.id(), distro.version(), distro.codename()
    if name == 'rhel':
        name = 'redhat'
    elif name in ('opensuse', 'sles', 'suse_linux', 'suse_sap'):
        name = 'suse'
    return name, version, codename
