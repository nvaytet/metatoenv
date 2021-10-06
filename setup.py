from setuptools import setup, Command

from distutils.command.build_py import build_py

with open('README.md') as infile:
    long_description = infile.read()

from psrecord import __version__

setup(
    name='metatoenv',
    version=__version__,
    description=
    'Generate a conda environment file from a conda meta.yaml recipe',
    long_description=long_description,
    url='https://github.com/nvaytet/metatoenv',
    license='BSD-3-Clause',
    author='Neil Vaytet',
    packages=['metatoenv'],
    provides=['metatoenv'],
    scripts=['scripts/metatoenv'],
    cmdclass={'build_py': build_py},
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
    ],
)
