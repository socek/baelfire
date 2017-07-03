# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'morfdict>=0.4.1',
    'jinja2',
    'pyyaml',
]

if __name__ == '__main__':
    setup(
        name='baelfire',
        version='0.5.1',
        description=("Tool for build automatization and a task runner"),
        author='Dominik "Socek" Długajczyk',
        author_email='msocek@gmail.com',
        packages=find_packages(),
        install_requires=install_requires,
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
