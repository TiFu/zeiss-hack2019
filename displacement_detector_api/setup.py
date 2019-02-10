#!/usr/bin/env python
import os
from setuptools import setup, find_packages

# install with pip install .

options = []
options.append('djangorestframework==3.8.2')






setup(
    name='displacement_detector_api',
      version='0.1',
      packages=find_packages(),
      install_requires=options+[
            'django==1.11',
            'psycopg2==2.7.4',
            'ruamel.yaml==0.15.50',
            'django-cors-headers==2.4.0',
            'django_filter==2.0.0',
            'pillow',
            'pandas',
            'numpy',
      ],
      extras_require={
          'local': options+['django-debug-toolbar==1.9.1'],
      }
    )
