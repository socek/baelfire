# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'morfdict>=0.4.1',
    'pytest',
    'jinja2',
    'mock',
    'pytest-cov',
    'pyyaml',
]

if __name__ == '__main__':
    setup(
        name='baelfire',
        version='0.4.1',
        description=("Makefile for python."),
        author='Dominik "Socek" Długajczyk',
        author_email='msocek@gmail.com',
        packages=find_packages(),
        install_requires=install_requires,
        test_suite='baelfire.tests.get_all_test_suite',
        license='Apache License 2.0',
        package_data={
            '': ['baelfire/application/commands/graph/tests/*.txt'],
        },
        entry_points={
            'console_scripts': [
                'bael=baelfire.application.application:run',
            ]
        },
    )
