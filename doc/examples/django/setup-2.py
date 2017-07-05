# -*- encoding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

install_requires = [
    'baelfire==0.5.1',
    'Django==1.11.2',
    'celery==4.0.2',
]

if __name__ == '__main__':
    setup(
        name='bdjango',
        packages=find_packages(),
        install_requires=install_requires,
        entry_points={
            'console_scripts': [
                'bdcmd=bdjango.cmd:run',
            ]
        },
    )
