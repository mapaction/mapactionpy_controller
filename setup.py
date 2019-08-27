import subprocess
from setuptools import setup, find_packages
from os import path


def readme():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md')) as f:
        return f.read()


def get_git_revision_short_hash():
    ver = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
    return ver.decode('ascii').strip()


setup(name='mapactionpy_controller',
      version='0.1-dev{}'.format(get_git_revision_short_hash()),
      description='Controls the workflow of map and infographic production',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='http://github.com/mapaction/mapactionpy_controller',
      author='MapAction',
      author_email='github@mapaction.com',
      license='GPL3',
      packages=find_packages(),
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
