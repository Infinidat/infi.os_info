__import__("pkg_resources").declare_namespace(__name__)

from . import platform

# These versions of Ubuntu may not provide a short form
# of the OS codename in the /etc/os-release file.
UBUNTU_CODE_NAMES = {
    'Trusty Tahr': 'trusty',
    'Xenial Xerus': 'xenial',
    'Bionic Beaver': 'bionic',
    'Focal Fossa': 'focal',
    'Jammy Jellyfish': 'jammy',
    'Noble Numbat': 'noble'
}


def get_platform_name(platform_module=platform):
    """Returns the system name."""
    return platform_module.system().lower().replace('-', '').replace('_', '')


def system_is_rhel_based(platform_module=platform):
    """Checks if the OS is a RHEL-based distribution.

    :param platform_module: a platform-like module that
        implements system, architecture, processor,
        release, mac_ver and linux_distribution
    """
    system = get_platform_name(platform_module=platform_module)
    if system == 'linux':
        name, _, _ = platform_module.linux_distribution()
        if name in ('redhat', 'centos', 'oracle', 'rocky', 'almalinux', 'eurolinux'):
            return True
    return False


def get_platform_string(platform_module=platform):
    """Returns platform string: system-version-arch.

    :param platform_module: a platform-like module that
        implements system, architecture, processor,
        release, mac_ver and linux_distribution
    """
    system = get_platform_name(platform_module=platform_module)
    if system == 'linux':
        dist, version, codename = platform_module.linux_distribution()
        if dist == 'ubuntu':
            version = UBUNTU_CODE_NAMES.get(codename, codename)
        else:
            version = version.split('.')[0]
        processor = platform_module.processor()
        arch = processor if 'ppc' in processor else \
               ('x86' if '32bit' in platform_module.architecture() else 'x64')
        return "-".join([system, dist, version , arch])
    if system == 'windows':
        arch = 'x86' if '32bit' in platform_module.architecture() else 'x64'
        return "-".join([system, arch])
    if system == 'darwin':
        dist_version, _, arch = platform_module.mac_ver()
        dist_version = '.'.join(dist_version.split('.')[:2])
        if arch == 'x86_64':
            arch = 'x64'
        elif arch == 'arm64':
            pass  # Stay arm64
        else:
            arch = 'x86'
        return "-".join(["osx", dist_version, arch])
    if system == 'sunos':
        arch = 'sparc' if platform_module.processor() == 'sparc' else \
               ('x86' if '32bit' in platform_module.architecture() else 'x64')
        # >>> platform.uname()
        # ('SunOS', 'host-ci17', '5.11', '11.2', 'i86pc', 'i386')
        # ('SunOS', 'host-ci19', '5.10', 'Generic_147148-26', 'i86pc', 'i386')
        version = platform_module.uname()[2].split('.')[-1]
        return "-".join(['solaris', version, arch])
    if system == "aix":
        uname = platform_module.uname()
        # example of uname: ('AIX', 'aixio002', '1', '7', '0001A8CAD300', 'powerpc')
        return "{0}-{1[3]}.{1[2]}-{1[5]}".format(system, uname)
    return ''


def get_version_from_git():
    from infi.gitpy.exceptions import GitCommandFailedException

    def get_commit_describe(commit, match_pattern='v*'):
        try:
            cmd = 'git describe --tags --match %s %s' % (match_pattern, commit)
            returned = commit.repo._executeGitCommandAssertSuccess(cmd).stdout.read().strip()
        except GitCommandFailedException:
            returned = commit.repo._executeGitCommandAssertSuccess(cmd.replace('*', '\*')).stdout.read().strip()
        all_tags = set(tag.name for tag in commit.repo.getTags())
        if returned not in all_tags:
            last_tagged_version, number_of_commits_after_tag, commit_hash = returned.rsplit("-", 2)
            returned = "{0}.post{1}".format(last_tagged_version, number_of_commits_after_tag)
        return returned

    def extract_version_tag_from_git():
        from infi.gitpy import LocalRepository
        from os import curdir, path
        repository = LocalRepository(curdir)
        branch = repository.getCurrentBranch()
        head = repository.getHead()
        if branch is None:
            return get_commit_describe(head)
        current_branch = branch.name
        stripped_branch = current_branch.split('/')[0]
        if stripped_branch in ('release', 'support', 'hotfix'):
            return get_commit_describe(head)
        if 'master' in stripped_branch:
            return get_commit_describe(head)
        else:
            try:
                return get_commit_describe(head, 'v*')
            except:
                pass
            return get_commit_describe(head)
        pass

    return extract_version_tag_from_git()


def get_version_from_file(filepath):
    with open(filepath) as fd:
        exec(fd.read())
    return locals()['__version__']


def shorten_version_string(version_string):
    from .parse_version import parse_version
    from re import split
    version_numbers = []
    parsed_version = list(parse_version(version_string))
    for item in parsed_version:
        if not item.isdigit():
            break
        version_numbers.append(int(item))
    last_index = len(version_numbers)
    while len(version_numbers) < 3:
        version_numbers.append(0)
    for item in parsed_version[last_index:]:
        if item.isdigit():
            version_numbers.append(int(item))
            break
    return '.'.join([str(item) for item in  version_numbers])


__all__ = ['get_platform_name', 'system_is_rhel_based',
           'get_platform_string', 'get_version_from_git',
           'get_version_from_file', 'shorten_version_string']
