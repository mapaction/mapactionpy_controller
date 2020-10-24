import importlib
import subprocess
import sys
from setuptools import setup, find_packages
from os import path, environ

_base_version = '1.0.4'

root_dir = path.abspath(path.dirname(__file__))


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


def get_gis_environment():
    gis_dependancies = []

    # The key is the module name that is detected
    # The value is the module name that will be installed if the key is detected.
    possible_envs = {
        'arcpy': 'mapactionpy_arcmap',
        'qgis.core': 'mapactionpy_qgis'
    }

    for env_mod, target_mod in possible_envs.items():
        sys.stderr.write('\nsys.path={}\n'.format(sys.path))
        try:
            sys.stderr.write('\ntrying to import {}\n'.format(env_mod))
            importlib.import_module(env_mod)
            gis_dependancies.append(target_mod)
            sys.stderr.write('\nsucessed importing {}, added {} to gis_dependancies\n'.format(env_mod, target_mod))
        except ImportError:
            sys.stderr.write('\nfailed to import {}\n'.format(env_mod))
            # pass

    return gis_dependancies


setup(
    name='mapactionpy_controller',
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
    install_requires=[
        'chevron',
        'humanfriendly',
        'jsonpickle',
        'jsonschema',
        'pyrsistent<=0.16.1',
        'pycountry<=19.8.18',
        'requests',
        'pyyaml',
        'six',
        'slugify'
    ],
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
