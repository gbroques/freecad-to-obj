import io
from os import path

from setuptools import setup

version = {}
with open('freecad_to_obj/_version.py') as fp:
    exec(fp.read(), version)

current_dir = path.abspath(path.dirname(__file__))
with io.open(path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='freecad-to-obj',
    description='Export FreeCAD models to the Wavefront (.obj) file format.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gbroques/freecad-to-obj',
    author='G Roques',
    version=version['__version__'],
    packages=['freecad_to_obj'],
    # Incude data files specified in MANIFEST.in file.
    include_package_data=True,
    install_requires=[],
    classifiers=[
        # Full List: https://pypi.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3 :: Only'
    ]
)
