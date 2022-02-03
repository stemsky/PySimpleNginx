from setuptools import setup, find_packages

setup(
    name='PySimpleNginx',
    version='0.2.1',
    description='A simple nginx config and control module',
    url='https://github.com/stemsky/PySimpleNginx.git',
    author='stemsky',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages()
)
    