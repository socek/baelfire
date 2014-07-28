# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
from baelfire import VERSION

install_requires = [
    'smallsettings',
    'soktest',
    'jinja2',
]

if __name__ == '__main__':
    setup(name='baelfire',
          version=VERSION,
          description=
          "Make like program, which reads python script as a makefile.",
          author='Dominik "Socek" Długajczyk',
          author_email='msocek@gmail.com',
          packages=find_packages(),
          install_requires=install_requires,
          test_suite='baelfire.tests.get_all_test_suite',
          license='Apache License 2.0',
          entry_points="""\
              [console_scripts]
                  bael = baelfire.application.application:run
          """,
          )
