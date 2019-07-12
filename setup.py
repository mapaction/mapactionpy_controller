from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='mapactionpy_controller',
      version='0.1',
      description='Controls the workflow of map and infographic production',
      url='http://github.com/mapaction/mapactionpy_controller',
      author='MapAction',
      author_email='github@mapaction.com',
      license='GPL3',
      packages=['mapactionpy_controller'],
	  test_suite='unittest',
      tests_require=['unittest'],
      zip_safe=False)