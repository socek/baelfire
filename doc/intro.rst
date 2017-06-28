=================
1. About Baelfire
=================

1.1 What is Baelfire
--------------------
Baelfire is a tool for build automatization. It can be used instead of GNU Make.

1.2 Why reimplement makefile?
-----------------------------
Creating dependency hierarchy in makefile can be tricky, when project has very similar files and all you want to do is
build most of them in the same way. That is why most of the projects use some tool to generate makefiles.
Also, make supports only "if file is newear, then rebuild". Baelfire tasks are implemented in python, so dependency can
be more then just checking file's mtime.

Your tasks can be more then just "build a file". Baelfire supports tasks like generating files from templates and making
algorithms for dependency (e.g. run migration if there is a new migration file). That is why you can use Baelfire
for running developer's servers.
Baelfire also implements report feature, to let you know what happend during the run.

1.3 Advantage of Baelfire
-------------------------
* more powerful dependency due to implementation in python
* simpler debbuging due to the report feature
* report feature can create graph
* template tasks
* dependency system which is easy to expand

1.4 Website
-----------
Baelfire do not have any special project website, by we have a github projcet here:
https://github.com/socek/baelfire

1.5 Install
-----------
You can install using easy_install:

>>> easy_install baelfire

or pip:

>>> pip install baelfire
