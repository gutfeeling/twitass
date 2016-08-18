#!/usr/bin/env python

from setuptools import setup

setup(name = "twitass",
      version = "1.0",
      description = "scrapes tweets from the twitter advanced search webpage",
      author = "Dibya Chakravorty",
      author_email = "dibyachakravorty@gmail.com",
      url = "https://github.com/gutfeeling/twitass",
      install_requires = ["requests>=2.10.0",
                          "beautifulsoup4>=4.5.0"],
     )
