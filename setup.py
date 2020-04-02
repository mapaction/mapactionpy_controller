import distutils.version as version
import importlib
import subprocess
from setuptools import setup, find_packages
from os import path, environ


def readme():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md')) as f:
        return f.read()


_base_version = '0.10'


def _get_version_number():
    travis_build = environ.get('TRAVIS_BUILD_NUMBER')
    travis_tag = environ.get('TRAVIS_TAG')

    if travis_build:
        if travis_tag:
            return travis_tag
        else:
            return '{}.dev{}'.format(_base_version, travis_build)
    else:
        try:
            ver = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
            return '{}+local.{}'.format(_base_version, ver.decode('ascii').strip())
        except Exception:
            return ''


def get_install_requires():
    dependancies = [
        'jsonpickle',
        'six'
    ]
    dependancies.append(get_gis_environment())

    return dependancies


def get_gis_environment():
    gis_dependancies = []
    v = version.StrictVersion(_base_version)
    next_minor_version = '{}.{}'.format(v.version[0], v.version[1]+1)

    # The key is the module name that is detected
    # The value is the module name that will be installed if the key is detected.
    possible_envs = {
        'arcpy': 'mapactionpy_arcmap',
        'qgis.core': 'mapactionpy_qgis'
    }

    for env_mod, target_mod in possible_envs.items():
        try:
            importlib.import_module(env_mod)
            gis_dependancies.append('{}>={},<{}'.format(target_mod, _base_version, next_minor_version))
        except ImportError:
            pass

    return gis_dependancies


setup(name='mapactionpy_controller',
      version=_get_version_number(),
      description='Controls the workflow of map and infographic production',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='http://github.com/mapaction/mapactionpy_controller',
      author='MapAction',
      author_email='github@mapaction.com',
      license='GPL3',
      packages=find_packages(),
      install_requires=get_install_requires(),
      test_suite='unittest',
      tests_require=['unittest'],
      zip_safe=False,
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
      ])
