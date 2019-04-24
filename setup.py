#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='wagtail-import-export',
    version='0.2',
    description="Page export from one Wagtail instance into another",
    author='Torchbox and NHS Digital',
    author_email='hello@torchbox.com',
    url='https://github.com/torchbox/wagtail-import-export',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django",
        "wagtail",
    ],
    tests_require=[
        "factory-boy==2.11.1",
        "wagtail-factories==1.1.0",
    ]
    license='BSD',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
)
