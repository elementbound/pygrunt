version_tuple = (0,5,7)
version_str = '.'.join([str(x) for x in version_tuple])
version = version_str

def _get_gitinfo():
    import pygrunt.platform as platform
    import subprocess
    from pathlib import Path

    git = platform.current.find_executable('git')
    if git is None:
        # No git installed; assume we're on master
        return ('master', '')

    cwd = str(Path(__file__).parent)

    args = [git, 'rev-parse', '--abbrev-ref', 'HEAD']
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=cwd, universal_newlines=True)
    if result.returncode != 0:
        # Quietly return defaults on fail
        return ('master', '')

    branch = result.stdout

    args = [git, 'rev-parse', 'HEAD']
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, cwd=cwd, universal_newlines=True)
    if result.returncode != 0:
        # Quietly return defaults on fail
        return ('master', '')

    commit = result.stdout

    return (branch.strip(), commit.strip())

branch, commit = _get_gitinfo()
