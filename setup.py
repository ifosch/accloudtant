from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# TODO: Review
#  https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='accloudtant',
    version='0.0.1.dev1',
    description='Cloud cost calculation tool',
    long_description=long_description,
    url='https://github.com/ifosch/accloudtant',
    install_requires=['requests'],
    scripts=['bin/accloudtant'],
)
