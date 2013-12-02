#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from setuptools import setup

setup(
  name = 'TracZurbTheme',
  version = '1.0',
  packages = ['zurbtheme'],
  package_data = {'zurbtheme': ['htdocs/*.*', 'htdocs/css/*.woff', 'htdocs/css/*.css', 'htdocs/js/*.js',
                                'htdocs/img/*.*', 'templates/*.html']},

  author = "Jorge Luis Casado Gandolff",
  author_email = 'jcasado81@gmail.com',
  maintainer = 'Jorge Luis',
  maintainer_email = 'jcasado81@gmail.com',
  description = "Theme Zurb (Trac)",
  license = "BSD",
  keywords = "trac plugin theme zurb foundation",
  url = "https://github.com/nothingagency/trac-zurbtheme",
  classifiers = [
      'Framework :: Trac',
    ],
  install_requires = ['TracThemeEngine'],
  entry_points = {
      'trac.plugins': [
            'zurbtheme.theme = zurbtheme.theme',
        ]}
)
