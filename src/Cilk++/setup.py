# call with
# sage -python setup.py build_ext --inplace

import os, sys

try:
    CILK_ROOT = os.environ['CILK_ROOT']
except KeyError:
    raise EnvironmentError, "Please define the CILK_ROOT environment variable !"
# setup the gcc/cilk compiler
os.environ['CC'] = os.path.join(CILK_ROOT, 'bin', 'g++')

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from distutils.extension import Extension
from sage.env import *

SAGE_INC = os.path.join(SAGE_LOCAL, 'include')
SAGE_C   = os.path.join(SAGE_SRC, 'c_lib', 'include')
SAGE_DEV = os.path.join(SAGE_ROOT, 'devel', 'sage-main')
CILK_LIB = os.path.join(CILK_ROOT, 'lib64')

import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension('numeric_monoid',
                  sources = ['numeric_monoid.pyx', 'monoid.cpp', 'treewalk.cpp'],
                  language="c++",
                  include_dirs = [SAGE_C,SAGE_DEV],
                  extra_compile_args = ['-std=c++0x', '-O3',
                                        '-march=native', '-mtune=native',
                                        '-fcilkplus'],
                  library_dirs = [CILK_LIB],
                  runtime_library_dirs = [CILK_LIB],
                  libraries = ['csage', 'cilkrts'],
                  depends = ['monoid.hpp', 'treewalk.hpp', 'cppmonoid.pxd'],
                  define_macros = [('NDEBUG', '1'), ('MAX_GENUS','86')],
                  ),
        ])

