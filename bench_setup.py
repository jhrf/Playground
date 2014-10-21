from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'bench_sam',
  ext_modules = cythonize("mate_retrieve_benchmark.py"),
)