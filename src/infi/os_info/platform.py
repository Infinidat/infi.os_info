# Module with same api as built-in platform but different implementation of linux_distribution that uses distro's one.
from __future__ import absolute_import
from platform import *


def linux_distribution():
    import distro
    id_name, version, codename = distro.linux_distribution(full_distribution_name=False)
    # distro returns rhel instead of redhat and sles instead of suse
    id_name = id_name.replace('rhel', 'redhat').replace('sles', 'suse')
    return (id_name, version, codename)
