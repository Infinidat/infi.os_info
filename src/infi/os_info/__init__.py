__import__("pkg_resources").declare_namespace(__name__)

import platform


def get_platform_string(platform_module=platform):
    """:param platform_module: a platform-like module that implements system, architecture, processor, release, mac_ver, linux_distribution"""
    system = platform_module.system().lower().replace('-', '').replace('_', '')
    if system == 'linux':
        dist_long, version, version_id = platform_module.linux_distribution()
        # We remove the linux string for centos (so it won't be centoslinux)
        dist_name = ''.join(dist_long.split(' ')[:2]).lower().replace('linux','')
        if dist_name == 'ubuntu':
            dist_version = version_id
        elif dist_name == 'centos' or dist_name == 'redhat':
            dist_version = version.split('.')[0]
        else:
            dist_version = version.split('.')[0]
        arch = 'x86' if '32bit' in platform_module.architecture() else 'x64'
        return "-".join([system, dist_name, dist_version , arch])
    if system == 'windows':
        arch = 'x86' if '32bit' in platform_module.architecture() else 'x64'
        return "-".join([system, arch])
    if system == 'darwin':
        dist_version, _, arch = platform_module.mac_ver()
        dist_version = '.'.join(dist_version.split('.')[:2])
        arch = 'x64' if arch == 'x86_64' else 'x86'
        return "-".join(["osx", dist_version, arch])
    if system == 'sunos':
        arch = 'sparc' if platform_module.processor() == 'sparc' else \
               ('x86' if '32bit' in platform_module.architecture() else 'x64')
        return "-".join(['solaris', platform_module.release(), arch])
    return ''


def get_version_from_git():
    from gitpy.exceptions import GitCommandFailedException

    def get_commit_describe(commit, match_pattern='v*'):
        try:
            cmd = 'git describe --tags --match %s %s' % (match_pattern, commit)
            returned = commit.repo._executeGitCommandAssertSuccess(cmd).stdout.read().strip()
        except GitCommandFailedException:
            returned = commit.repo._executeGitCommandAssertSuccess(cmd.replace('*', '\*')).stdout.read().strip()
        all_tags = set(tag.name for tag in commit.repo.getTags())
        if returned not in all_tags:
            returned = "{0}.post{1}.{2}".format(*returned.rsplit("-", 2))
        return returned

    def extract_version_tag_from_git():
        from gitpy import LocalRepository
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
        exec fd.read()
    return locals()['__version__']


def shorten_version_string(version_string):
    from pkg_resources import parse_version
    version_numbers = []
    parsed_version = list(parse_version(version_string))
    for item in parsed_version:
        if not item.isdigit():
            break
        version_numbers.append(int(item))
    while len(version_numbers) < 3:
        version_numbers.append(0)
    index = parsed_version.index(item)
    for item in parsed_version[index:]:
        if item.isdigit():
            version_numbers.append(int(item))
            break
    return '.'.join([str(item) for item in  version_numbers])


__all__ = ['get_platform_string', 'get_version_from_git', 'get_version_from_file', 'shorten_version_string']
