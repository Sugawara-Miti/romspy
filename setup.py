# coding: utf-8
# (c) 2015 Teruhisa Okada

from distutils.core import setup

setup(name='romspy',
      version='1.3',
      description='Tools for ROMS with Python',
      author='Teruhisa Okada',
      author_email='okada@civil.eng.osaka-u.ac.jp',
      url='https://github.com/okadate/romspy/',
      packages=['romspy', 'romspy.boundary', 'romspy.convert', 'romspy.nest'])
