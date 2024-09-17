from infi import unittest
from mock import patch
import distro
from infi.os_info import system_is_rhel_based, platform


test_subjects = [
    dict(expected=True, system='Linux', architecture=('64bit', 'ELF'), processor='x86_64', release='5.14.0-362.8.1.el9_3.x86_64', mac_ver=('', ('', '', ''), ''), linux_distribution=('redhat', '9.3', 'Plow')),
    dict(expected=True, system='Linux', architecture=('64bit', 'ELF'), processor='x86_64', release='3.10.0-514.el7.x86_64', mac_ver=('', ('', '', ''), ''), linux_distribution=('centos', '7.9', 'CentOS')),
    dict(expected=True, system='Linux', architecture=('64bit', 'ELF'), processor='x86_64', release='5.14.0-427.22.1.el9_4.x86_64', mac_ver=('', ('', '', ''), ''), linux_distribution=('rocky', '9.4', 'Blue Onyx')),
    dict(expected=False, system='Windows', architecture=('64bit', 'WindowsPE'), processor='', release='2012Server', mac_ver=('', ('', '', ''), ''), linux_distribution=('', '', '')),
    dict(expected=False, system='Windows', architecture=('32bit', 'WindowsPE'), processor='', release='2008Server', mac_ver=('', ('', '', ''), ''), linux_distribution=('', '', '')),
    dict(expected=False, system='Linux', architecture=('64bit', 'ELF'), processor='x86_64', release='3.13.0-36-generic', mac_ver=('', ('', '', ''), ''), linux_distribution=('ubuntu', '14.04', 'trusty')),
    dict(expected=False, system='Linux', architecture=('64bit', 'ELF'), processor='x86_64', release='3.0.76-0.11-default', mac_ver=('', ('', '', ''), ''), linux_distribution=('suse', '12', 'x86_64')),
    dict(expected=False, system='Linux', architecture=('64bit', 'ELF'), processor='x86_64', release='3.0.76-0.11-default', mac_ver=('', ('', '', ''), ''), linux_distribution=('suse', '15', 'x86_64')),
    dict(expected=False, system='Solaris', architecture=('64bit', 'ELF'), processor='sparcv9', release='11.4', mac_ver=('', ('', '', ''), ''), linux_distribution=('', '', '')),
    dict(expected=False, system='SunOS', architecture=('32bit', 'ELF'), processor='i86pc', release='10.11', mac_ver=('', ('', '', ''), ''), linux_distribution=('', '', '')),
    dict(expected=False, system='Solaris', architecture=('64bit', 'ELF'), processor='sparcv9', release='11.4', mac_ver=('', ('', '', ''), ''), linux_distribution=('', '', '')),
    dict(expected=False, system='AIX', architecture=('64bit', 'XCOFF'), processor='powerpc', release='7.3', mac_ver=('', ('', '', ''), ''), linux_distribution=('', '', '')),
]


class FakePlatformModule(object):
    """:param platform_module: a platform-like module that implements system, architecture, processor, release, mac_ver, linux_distribution"""

    def __init__(self, system, architecture, processor, release, mac_ver, linux_distribution):
        self.system = lambda: system
        self.architecture = lambda: architecture
        self.processor = lambda: processor
        self.release = lambda: release
        self.mac_ver = lambda: mac_ver
        self.linux_distribution = lambda: linux_distribution


class PlatformStringTestCase(unittest.TestCase):
    @unittest.parameters.iterate('test_subject', test_subjects)
    def test_platform_string(self, test_subject):
        copy_subject = test_subject.copy()
        expected = copy_subject.pop('expected')
        self.assertEquals(expected, system_is_rhel_based(FakePlatformModule(**copy_subject)))


class TestGetPlatformString(unittest.TestCase):
    """A deeper test of all the pipe of system_is_rhel_based"""
    @unittest.parameters.iterate('test_subject', test_subjects)
    def test_system_is_rhel_based(self, test_subject):
        with patch("distro.id") as distro_id,\
             patch("distro.version") as distro_version, \
             patch("distro.codename") as distro_codename, \
                                        patch("infi.os_info.platform.system") as platform_system,\
                                        patch("infi.os_info.platform.architecture") as platform_architecture,\
                                        patch("infi.os_info.platform.processor") as platform_processor,\
                                        patch("infi.os_info.platform.release") as platform_release,\
                                        patch("infi.os_info.platform.mac_ver") as platform_mac_ver:
            distro_id.return_value = test_subject['linux_distribution'][0]
            distro_version.return_value = test_subject['linux_distribution'][1]
            distro_codename.return_value = test_subject['linux_distribution'][2]
            platform_system.return_value = test_subject['system']
            platform_architecture.return_value = test_subject['architecture']
            platform_release.return_value = test_subject['processor']
            platform_release.return_value = test_subject['release']
            platform_mac_ver.return_value = test_subject['mac_ver']
            expected = test_subject['expected']
            self.assertEquals(expected, system_is_rhel_based())
