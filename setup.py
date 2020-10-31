import subprocess
import sys
from setuptools import setup, find_packages
# from setuptools import find_packages
# from distutils.cmd import Command
# from distutils.command.install import install as Command
from setuptools.command.develop import develop
from setuptools.command.install import install
# from distutils.core import setup
from os import path, environ

_base_version = '1.0.4'

root_dir = path.abspath(path.dirname(__file__))


def install_from_wheels(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.

    It modifies the run() method so that it prints a friendly greeting.

    https://blog.niteo.co/setuptools-run-custom-code-in-setup-py/
    """
    orig_run = command_subclass.run

    def modified_run(self):
        print('Custom run() method')

        if (sys.version_info.major == 2) and (sys.platform == 'win32'):
            import pip
            # The order these packages are intalled  matters, which is why
            # this does just do something like
            # `glob.glob('{}/dependancy_wheels/*.whl'.format(root_dir))`
            wheel_list = [
                'pyproj-1.9.6-cp27-cp27m-win32.whl',
                'Shapely-1.6.4.post2-cp27-cp27m-win32.whl'
            ]

            for wheel_name in wheel_list:
                wheel_path = path.join(root_dir, 'dependency_wheels', wheel_name)
                print('Installing {} from wheel file.'.format(wheel_path))
                pip.main(['install', wheel_path])

        print('About to call default install run() method')
        orig_run(self)

    command_subclass.run = modified_run
    return command_subclass


@install_from_wheels
class CustomDevelopCommand(develop):
    pass


@install_from_wheels
class CustomInstallCommand(install):
    pass


def readme():
    with open(path.join(root_dir, 'README.md')) as f:
        return f.read()


# See https://packaging.python.org/guides/single-sourcing-package-version/
# This uses method 4 on this list combined with other methods.
def _get_version_number():
    travis_build = environ.get('TRAVIS_BUILD_NUMBER')
    travis_tag = environ.get('TRAVIS_TAG')

    if travis_build:
        if travis_tag:
            version = travis_tag
        else:
            version = '{}.dev{}'.format(_base_version, travis_build)

        with open(path.join(root_dir, 'VERSION'), 'w') as version_file:
            version_file.write(version.strip())
    else:
        try:
            ver = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
            version = '{}+local.{}'.format(_base_version, ver.decode('ascii').strip())
        except Exception:
            with open(path.join(root_dir, 'VERSION')) as version_file:
                version = version_file.read().strip()

    return version


def _get_requires_list():
    # Items for which the version does not need to be pinned to support py2.7
    requires = [
        'chevron',
        'humanfriendly',
        'jsonpickle',
        'jsonschema',
        'requests',
        'pyyaml',
        'six',
        'slugify'
    ]

    if (sys.version_info.major == 2):
        # Items for which do need a pinned version to support py2.7
        # For debate whether this is useful 'pyreproj==1.0.1'
        requires.extend([
            'pyrsistent<=0.16.1',
            'pycountry<=19.8.18'
        ])
    else:
        # The same items but for py3.x
        requires.extend([
            'pyrsistent',
            'pycountry',
            'pyproj',
            'Shapely'

        ])

    return requires


setup(
    name='mapactionpy_controller',
    cmdclass={
        'install': CustomInstallCommand,
        'develop': CustomDevelopCommand,
    },
    version=_get_version_number(),
    description='Controls the workflow of map and infographic production',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='http://github.com/mapaction/mapactionpy_controller',
    author='MapAction',
    author_email='github@mapaction.com',
    license='GPL3',
    entry_points={
        'console_scripts': [
            'mapchef=mapactionpy_controller.cli:entry_point'
        ]
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=_get_requires_list(),
    test_suite='unittest',
    tests_require=['unittest'],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ])
