#!/usr/bin/env python

# Installation file

# Copyright (C) 2016-2017 Jorge Maldonado Ventura

# This file is part of Bullet Dodger

# Bullet dodger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Bullet dodger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Bullet dodger.  If not, see <http://www.gnu.org/licenses/>.


import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='bullet_dodger',
    version=__import__('bullet_dodger').__version__,
    author='Jorge Maldonado Ventura',
    author_email='jorgesumle@freakspot.net',
    description=__import__('bullet_dodger').PROGRAM_DESCRIPTION,
    entry_points={
        'console_scripts': [
            'bullet_dodger=bullet_dodger.bullet_dodger:main_loop'
        ],
    },
    license='GNU General Public License v3 (GPLv3)',
    keywords='videogame bullet action arcade simple',
    url='https://notabug.org/jorgesumle/bullet_dodger',
    packages=['bullet_dodger'],
    install_requires=[
        'pygame >= 1.9.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Arcade',
        'Topic :: Software Development :: Libraries :: pygame'
    ],
    include_package_data=True,
)
