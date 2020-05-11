# coding: utf-8
# (c) 2020-05-11 Teruhisa Okada

from distutils.core import setup


setup(name='romspy',
      version='2.1',
      description='Tools for ROMS with Python',
      author='Teruhisa Okada',
      author_email='okadate@gmail.com',
      url='https://github.com/okadate/romspy/',
      packages=['romspy', 'romspy.convert', 'romspy.hview', 'romspy.make', 'romspy.profile', 'romspy.tplot'])
