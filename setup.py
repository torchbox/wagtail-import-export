#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='wagtail-import-export',
    version='0.1',
    description="Page export from one Wagtail instance into another",
    author='Torchbox and NHS Digital',
    author_email='hello@torchbox.com',
    url='https://github.com/torchbox/wagtail-import-export',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
)
