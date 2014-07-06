=================
1. About Baelfire
=================

1.1 Why reimplement makefile?
=============================
Setting dependency in makefile is not flexible. Supports only "if file is newear,
then rebuild". Baelfire can have, in it's dependency, whatever python code you want.
Event if you want to check something using network.

1.2 Advantage of Baelfire
=====================
* more flexible dependency
* can use python code for dependecy
* simpler debbuging
* can draw tasks graphs

1.3 Website
===========
Baelfire do not have any special project website, by we have a github projcet here:
https://github.com/socek/baelfire

1.4 Install
===========
You can install using easy_install:

>>> easy_install baelfire

or pip:

>>> pip install baelfire
