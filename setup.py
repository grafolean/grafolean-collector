import os
from setuptools import setup, find_packages

requirements_txt = os.path.dirname(os.path.realpath(__file__)) + '/requirements.txt'
with open(requirements_txt, "rt") as f:
    install_requires = f.read().splitlines()[1:]

setup(name='grafoleancollector',
      version='@@VERSION@@',
      url='https://gitlab.com/grafolean/grafolean-collector',
      license='Commons Clause + Apache 2.0',
      author='Anže Škerlavaj',
      author_email='info@grafolean.com',
      description='Common utilities for creating (controlled) collectors for Grafolean',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      install_requires=install_requires,
      zip_safe=False)