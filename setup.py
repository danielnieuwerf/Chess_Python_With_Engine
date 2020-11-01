from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("CythonGame.pyx")
)
setup(
    ext_modules = cythonize("CythonCharBoard.pyx")
)
setup(
    ext_modules = cythonize("CythonBitBoard.pyx")
)
setup(
    ext_modules = cythonize("CythonScores.pyx")
)