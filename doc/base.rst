2.1 Simple Tasks
================

2.1.1 First task
----------------
Making tasks is very simple. Just inherite from Task, and implement two methods:

* create_dependecies(self)
    This method creates dependency for the task, for example "rebuild on file change".
* build(self)
    This method is executed when the task dependency result is "true for rebuild".

.. literalinclude:: code/doc1.py
    :language: python
    :caption: doc1.py
    :linenos:

* line 8: create dependency which say "rebuild if file does not exists".
* line 10: creating a build script: open a file, and write something to it.
* line 15-16: run the task if it is used from the command line.

.. code-block:: bash

    $ python doc1.py
    building...
    $ cat /tmp/me
    something
    $ python doc1.py
    $ rm /tmp/me
    $ python doc1.py
    building...

First we run the task to build a file. If the file is created, task does not
rebuild itself. But it will be rebuilded if the file is not present.

2.1.2 Logging
-------------

Tasks and dependencies has logging support. You can turn it on so the build will show much more informations.

.. literalinclude:: code/doc2.py
    :language: python
    :caption: doc2.py
    :linenos:

.. code-block:: bash

    $ python doc2.py
     * DEBUG __main__.FirstTask: Dependency baelfire.dependencies.file.FileDoesNotExists result: True *
     * DEBUG __main__.FirstTask: Need to run: True *
     * INFO __main__.FirstTask: Running *
    building...
    $ python doc2.py
     * DEBUG __main__.FirstTask: Dependency baelfire.dependencies.file.FileDoesNotExists result: False *
     * DEBUG __main__.FirstTask: Need to run: False *

First, the FileDoesNotExists dependency check if file exists. If not, then task
will be rebuilded.

2.1.3 Task dependency
---------------------

Now, you know how to create one task. But what if we want to create tasks
depending on the run of other tasks. This is where TaskRebuilded and RunTask
come in handy. TaskRebuilded run other task. If this task is rebuilded, our
task is rebuilded too. RunTask does not affect dependency checking of a
parent.

.. literalinclude:: code/doc3.py
    :language: python
    :caption: doc3.py
    :linenos:

.. code-block:: bash

    $ python doc3.py
     * INFO __main__.FirstTask: Running *
     * INFO __main__.SecondTask: Running *
     * INFO __main__.ParentTask: Running *
    $ python doc3.py
    $ rm /tmp/me
    $ python doc3.py
     * INFO __main__.FirstTask: Running *
     * INFO __main__.ParentTask: Running *
    $ rm /tmp/me_too
    $ python doc3.py
     * INFO __main__.SecondTask: Running *

First run just creates all files. After deleting :file:`/tmp/me` which was linked to
parent task by TaskRebuilded, we will se that FirstTask and ParentTask is
rebuilded. But if we remove :file:`/tmp/me_too` which was linked by RunTask, only
the SecondTask is rebuilded.
