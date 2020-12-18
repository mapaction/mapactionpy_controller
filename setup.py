import subprocess
import sys
from setuptools import setup, find_packages
from os import path, environ

_base_version = '1.1.0'

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


def can_import_geo_packages():
    try:
        # Test PyProj
        import pyproj  # noqa: F401

        # Test Shapely
        from shapely.geometry import box  # noqa: F401

        # Test GDAL
        from osgeo import gdal  # noqa: F401
        from osgeo import ogr  # noqa: F401
        from osgeo import osr  # noqa: F401
        from osgeo import gdal_array  # noqa: F401
        from osgeo import gdalconst  # noqa: F401

        # Test Fiona
        import fiona  # noqa: F401

        # Test RTree
        from rtree import index  # noqa: F401

        # Test geopandas
        import geopandas  # noqa: F401

        return True
    except ImportError:
        return False


def _get_requires_list():
    # Items for which the version does not need to be pinned to support py2.7
    requires = [
        'chevron',
        'humanfriendly',
        'jsonpickle',
        'jsonschema',
        'requests',
        'pyyaml',
        'pyshp',
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
        requires.extend([
            'pyrsistent',
            'pycountry',
        ])

    if sys.platform == 'win32' and not can_import_geo_packages():
        requires.extend([
            'mapactionpy_controller_dependancies@git+'
            'https://github.com/mapaction/mapactionpy_controller_dependencies.git'
        ])
    else:
        requires.extend([
            'Fiona',
            'pyproj',
            'Shapely'
        ])

        # Test the underlying version of GDAL, so that we can install the matching python bindings
        try:
            # Test the underlying version of GDAL, so that we can install the matching python bindings
            gdal_cmd_ver = subprocess.check_output(['gdal-config', '--version'])
            gdal_ver = gdal_cmd_ver.decode('ascii').strip()
            gdal_str = 'GDAL=={}'.format(gdal_ver)

        except OSError:
            # from osgeo import gdal  # noqa: F401
            # gdal_ver = gdal.__version__
            gdal_str = 'GDAL'

        requires.extend([gdal_str])

        requires.extend([
            'Rtree',
            'geopandas'
        ])

    return requires


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
    package_dir={'mapactionpy_controller': 'mapactionpy_controller'},
    package_data={'mapactionpy_controller': ['schemas/*.schema']},
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
