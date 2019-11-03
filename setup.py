from setuptools import setup, find_packages

setup(name='grafoleancollector',
      version='@@VERSION@@',
      url='https://gitlab.com/grafolean/grafolean-collector',
      license='Commons Clause + Apache 2.0',
      author='Anže Škerlavaj',
      author_email='info@grafolean.com',
      description='Common utilities for creating (controlled) collectors for Grafolean',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)