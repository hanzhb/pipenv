# -*- coding=utf-8 -*-
import os
import sys
import pipenv

from pprint import pprint
from .__version__ import __version__
from .core import project
from .pythonfinder import find_python_in_path, system_which
from .pep508checker import lookup
from .utils import get_python_executable_version


def print_utf(line):
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode('utf-8'))


def main():
    print('<details><summary>$ python -m pipenv.help output</summary>')
    print('')
    print('Pipenv version: `{0!r}`'.format(__version__))
    print('')
    print('Pipenv location: `{0!r}`'.format(os.path.dirname(pipenv.__file__)))
    print('')
    print('Python location: `{0!r}`'.format(sys.executable))
    print('')
    print('Other Python installations in `PATH`:')
    print('')
    for python_v in ('2.5', '2.6', '2.7', '3.4', '3.5', '3.6', '3.7'):
        found = find_python_in_path(python_v)
        if found:
            print('  - `{0}`: `{1}`'.format(python_v, found))
        found = system_which('python{0}'.format(python_v), mult=True)
        if found:
            for f in found:
                print('  - `{0}`: `{1}`'.format(python_v, f))
    print('')
    for p in ('python', 'python2', 'python3', 'py'):
        found = system_which(p, mult=True)
        for f in found:
            print('  - `{0}`: `{1}`'.format(get_python_executable_version(f), f))
    print('')
    print('PEP 508 Information:')
    print('')
    print('```')
    pprint(lookup)
    print('```')
    print('')
    print('System environment variables:')
    print('')
    for key in os.environ:
        print('  - `{0}`'.format(key))
    print('')
    print_utf(u'Pipenv–specific environment variables:')
    print('')
    for key in os.environ:
        if key.startswith('PIPENV'):
            print(' - `{0}`: `{1}`'.format(key, os.environ[key]))
    print('')
    print_utf(u'Debug–specific environment variables:')
    print('')
    for key in ('PATH', 'SHELL', 'EDITOR', 'LANG', 'PWD', 'VIRTUAL_ENV'):
        if key in os.environ:
            print('  - `{0}`: `{1}`'.format(key, os.environ[key]))
    print('')
    print('')
    print('---------------------------')
    print('')
    if project.pipfile_exists:
        print_utf(
            u'Contents of `Pipfile` ({0!r}):'.format(project.pipfile_location)
        )
        print('')
        print('```toml')
        with open(project.pipfile_location, 'r') as f:
            print(f.read())
        print('```')
        print('')
    if project.lockfile_exists:
        print('')
        print_utf(
            u'Contents of `Pipfile.lock` ({0!r}):'.format(
                project.lockfile_location
            )
        )
        print('')
        print('```json')
        with open(project.lockfile_location, 'r') as f:
            print(f.read())
        print('```')
    print('</details>')


if __name__ == '__main__':
    main()

