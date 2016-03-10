from codecs import open as copen
from os import path

from setuptools import setup

HERE = path.abspath(path.dirname(__file__))

# TODO: Review
#  https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
with copen(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='accloudtant',
    version='0.0.1.dev1',
    description='Cloud cost calculation tool',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/ifosch/accloudtant',
    install_requires=['requests', 'tabulate', 'click', 'boto3'],
    scripts=['bin/accloudtant'],
)
