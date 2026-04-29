#!/usr/bin/env python
"""Setup itmlogic package."""
from glob import glob
from os.path import basename, splitext
from pathlib import Path

from setuptools import find_packages
from setuptools import setup


def readme():
    """Read README contents."""
    return Path('README.md').read_text(encoding='utf-8')


setup(
    name='itmlogic',
    use_scm_version=True,
    license='MIT License',
    description='Longley-Rice irregular terrain propagation model',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Ed Oughton',
    author_email='edward.oughton@gmail.com',
    url='https://github.com/edwardoughton/itmlogic',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    python_requires='>=3.9',
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Utilities',
    ],
    keywords=[
        'Longley-Rice', 'propagation model', 'irregular terrain model'
    ],
    setup_requires=[
        'setuptools_scm'
    ],
    install_requires=[
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            # eg: 'snkit = snkit.cli:main',
        ]
    },
)
