from setuptools import setup, find_packages, Extension
from setuptools.command.test import test as TestCommand
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import sys

#cython = Extension('ea.cbenchmarks',
#    sources = ['ea/cbenchmarks.pyx'],
##    include_dirs = ['include/']
#)
sourcefiles = ['cec2013lsgo/cec2013.pyx']

sourcefiles += ['cec2013lsgo/eval_func.cpp', 'cec2013lsgo/Benchmarks.cpp']

for i in range(1, 16):
    sourcefiles += ['cec2013lsgo/F%d.cpp' %i] 


cec2013lsgo = Extension("cec2013lsgo.cec2013",
              sourcefiles,
	      language = "c++",
              extra_compile_args=["-std=c++0x"],
#	      extra_compile_args=["-Wall -pedantic -std=c++0x"],
              libraries=["m"]) # Unix-like specific



class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
	name='cec2013lsgo',
        version='0.1',
        author='Daniel Molina',
        author_email='daniel.molina@uca.es',
        description='Package for benchmark for the Real Large Scale Global Optimization session on IEEE Congress on Evolutionary Computation CEC\'2013',
        long_description=open('README.rst').read(),
        license='GPL V3',
        packages=['cec2013lsgo'],
        install_requires=['cython', 'numpy'],
        ext_modules=cythonize(cec2013lsgo),
	tests_require=['pytest'],
#	ext_modules=cythonize('benchmarks.pyx', annotated=True),
cmdclass={'build_ext': build_ext, 'test': PyTest},
	# Packaging options.
	#include_package_data = True,
	# Tests
	#tests_require=['pytest'],
)
