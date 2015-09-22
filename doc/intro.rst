=================
1. About Baelfire
=================

1.1 Why reimplement makefile?
-----------------------------
Creating dependency hierarchy in makefile is not very flexible. Supports only
"if file is newear, then rebuild". Baelfire is a python code, so dependency can
be more then just checking file mtime. You can even make more specyfic tasks,
like generating files from tamples or making algorithm for searching for
dependency. Baelfire tasks also writes datalog, to let you know what happend
during the run.

1.2 Advantage of Baelfire
-------------------------
* more flexible dependency due to python code
* simpler debbuging due to datalog

1.3 Website
-----------
Baelfire do not have any special project website, by we have a github projcet here:
https://github.com/socek/baelfire

1.4 Install
-----------
You can install using easy_install:

>>> easy_install baelfire

or pip:

>>> pip install baelfire
