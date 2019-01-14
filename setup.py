from setuptools import setup, find_packages, Extension

import os
import blocklist

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'MANIFEST.in'), 'w', encoding='utf-8') as f:
    f.write('include LICENSE.md\ninclude README.md\ninclude blocklist/*.hpp')

with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    description = f.read()

uimod = Extension(
    'ui', language='c++',
    sources=['blocklist/ui.cpp'], depends=['blocklist/ui.h'],
)

setup(
    name=blocklist.__name__,
    version=blocklist.__version__,
    description=blocklist.__doc__,
    long_description=description,
    url='https://github.com/Joffr3y/blocklist.git',
    author=blocklist.__author__,
    author_email='j-off@live.fr',
    license='GPL3',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: French',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7'
    ],
    keywords='python blocklist peer torrent transmission',
    entry_points={'console_scripts': ['blocklist = blocklist.main:main']},
    ext_modules=[uimod]
)
