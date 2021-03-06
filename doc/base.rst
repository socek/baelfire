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

Baelfire has a logging support. You can turn it on so the build will show much more informations.

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

Description:
    - Format: ``{dotted task}: Dependency {dotted dependency} result: {False/True}``
        This line is describing Dependency checking. ``{task}`` has checked ``{dependency}`` which resulted in
        ``{False}`` or ``{True}``.
    - Format: ``{dotted task}: Need to run: {False/True}``
        This line is showing result of all dependency checks. If at least one of the dependency will result in True,
        then whole task will be rebuilded.
    - Format: ``{dotted task}: Running``
        This line just shows when the task has started rebuilding.

2.1.3 Task dependency
---------------------

Now, you know how to create one task. But what if we want to create tasks depending on the run of other tasks. This is
where ``TaskRebuilded`` dependency come in handy. It runs other task and if the task is rebuilded, our parent task is
rebuilded too.

If we would like to just run a task before our parent task, then we should use ``Task.run_before`` method.

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

First run just creates all files. After deleting :file:`/tmp/me` which was linked to parent task by ``TaskRebuilded``,
we will see that FirstTask and ParentTask is rebuilded. But if we remove :file:`/tmp/me_too` which was linked by
``Task.run_before``, only the SecondTask is rebuilded and the ParentTask is not rebuilded.
