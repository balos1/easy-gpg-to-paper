#!/usr/bin/env python

from distutils.core import setup

setup(name='easy-gpg-to-paper',
      version='1.0.0',
      description='easy-gpg-to-paper aims to make exporting your secret gpg key to paper, and then restoring from paper, an easy and painless process.',
      author='Cody Balos',
      author_email='cjbalos@gmail.com',
      url='https://github.com/cojomojo/easy-gpg-to-paper',
      packages=['gpg2paper'],
      install_requires=['Pillow>=4', 'qrcode>=5', 'weasyprint>=0.38,<=1.0'],
)
