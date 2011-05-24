# encoding: utf-8

from setuptools import setup, find_packages
import sys, os

version = '0.1.0'
 
setup(
    name='columbo',
    version=version,
    description="WSGI Profiler",
    long_description="""Profiler for WSGI applications with a slick UI""",
    classifiers=[
        "Topic :: Software Development",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    keywords='',
    author='ESN Social Software AB',
    author_email='',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask"],

)
