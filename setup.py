#!/usr/bin/env python
from distutils.core import setup
import tourcms


setup(name='tourcms',
      version=tourcms.__version__,
      description="Python wrapper class for TourCMS Rest API",
      long_description="A simple wrapper for connecting to the TourCMS Marketplace API (http://www.tourcms.com/support/api/mp/). This wrapper mirrors the TourCMS PHP library. See https://github.com/prio/tourcms for more details.",
      author=tourcms.__author__,
      author_email='jonathan@jonharrington.org',
      url='https://github.com/prio/tourcms',
      download_url='https://github.com/prio/tourcms',
      license=tourcms.__license__,
      platforms=['all'],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
      ],
      py_modules=['tourcms'],
      )