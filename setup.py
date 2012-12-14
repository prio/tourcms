#!/usr/bin/env python

from distutils.core import setup
import tourcms

setup(name='tourcms',
      version=tourcms.__version__,
      description=tourcms.__doc__,
      author=tourcms.__author__,
      author_email='jonathan@jonharrington.org',
      url='https://github.com/prio/tourcms',
      license=tourcms.__license__,
      platforms=['all'],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
      ],
      py_modules=['tourcms'],
      )