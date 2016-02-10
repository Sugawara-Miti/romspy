# coding: utf-8
# (c) 2015 Teruhisa Okada

from distutils.core import setup

setup(name='romspy',
      version='2.0',
      description='Tools for ROMS with Python',
      author='Teruhisa Okada',
      author_email='okada@civil.eng.osaka-u.ac.jp',
      url='https://github.com/okadate/romspy/',
      packages=['romspy', 'romspy.convert', 'romspy.hview', 'romspy.make', 'romspy.profile', 'romspy.tplot'])
