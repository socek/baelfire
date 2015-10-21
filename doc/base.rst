2.1 Base
========

2.1.1 First task
----------------
Making tasks is very simple. Just inherite from Task, and implement two methods:

* create_dependecies(self)
    This is where you put your dependecies, for example "rebuild on file change".
* build(self)
    This is where you build your task.

.. literalinclude:: code/doc1.py
    :language: python
    :caption: doc1.py
    :linenos:

In line 8 we create dependency which say "rebuild if file does not exists".
In line 10 we creating a build script. Only thing which we are doing here is
open a file, and write something to it.
In line 15 we are running the task, so we can run it in the command line.

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

Task and dependencies has logging support. You can turn it on, and see what
happend.

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

You now know how to create one task. But what if we want to create tasks
depending on running other tasks. This is where TaskDependency and RunBefore
come in handy. TaskDependency run other task. If this task is rebuilded, our
task is rebuilded too. RunBefore does not affect dependency checking of a
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
parent task by TaskDependency, we will se that FirstTask and ParentTask is
rebuilded. But if we remove :file:`/tmp/me_too` which was linked by RunBefore, only
the SecondTask is rebuilded.

2.1.4 Settings
--------------

Task class use `MorfDict <https://pythonhosted.org/MorfDict/>`_ ``StringDict``
and ``PathDict`` for settings and paths. All linked tasks have the same settings
and paths object, so we can edit in the parent if we want.

.. literalinclude:: code/doc4.py
    :language: python
    :caption: doc4.py
    :linenos:

.. code-block:: bash

    $ python doc4.py
    S my parent
    S /base/first.txt
    P my parent
    P /base/first.txt

We create 2 tasks and make settings for both of them. From Parent task we can
ovveride some settings within a child tasks.

2.1.5 FileDict - saving settings to a file
------------------------------------------

Sometimes settings can be saved to a file and retrived from there. For example,
name of the project we need only at the start and we can retrive it from disk
next time.

.. literalinclude:: code/doc11.py
    :language: python
    :caption: doc11.py
    :linenos:

.. code-block:: bash
    $ (master ✗) $ python doc11.py
    Description for something: testme
    testme
    $ (master ✗) $ python doc11.py
    testme
    $ (master ✗) $
