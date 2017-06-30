5.1 Django
==========

When we are implementing simple Django application and we want to start developer server, we need to make some steps
before actual running:

- update requiretments from setup.py or requiretments.txt
- make migrations
- start celery
- start runserver

Using baelfire we can automate this process so all these steps will be made before the runserver but only when needed.


5.1.1 Create the application
----------------------------

First of all, we need to create simple Django application for tests. It will not have any views, because all we want is
to make sure the runserver will start. We will not go into details here, because it is not a Django tutorial. So we will
start with the setup.py file.

.. literalinclude:: django/setup-1.py
    :language: python
    :caption: setup.py
    :linenos:

I like to have simple makefile to create virtualenv and install first, so here it is:

.. literalinclude:: django/makefile-1
    :language: makefile
    :caption: Makefile
    :linenos:

Now we can run it and activate virtualenv.

.. literalinclude:: django/run-1

Now we can create our application and start runserver.

.. literalinclude:: django/run-2

Our simple Django application is ready.

5.1.2 Baelfire package and first task
-------------------------------------

First step in creating automatizion is to create package that will be outside of the django app, which we created a
moment ego.

.. literalinclude:: django/run-3

And the first task which will run ``python setup.py develop``

.. literalinclude:: django/tasks-1.py
    :language: python
    :caption: bdjango/tasks.py
    :linenos:

Now we can start our first task and see what it will do:

.. literalinclude:: django/run-4

Ok, but now we have hardcoded path for python executable, and hardcoded path for setup.py. This will not work if we
change our workdir.

.. literalinclude:: django/run-5

So now we will create ``Core`` class and do some path configurations.

.. literalinclude:: django/core-1.py
    :language: python
    :caption: bdjango/core.py
    :linenos:

At line 9 we are setting the main project path. The rest of the paths are created depending on this main path. Now we
need to implement these settings in our task.

.. literalinclude:: django/tasks-2.py
    :language: python
    :caption: bdjango/tasks.py
    :linenos:

Last step for this paragraph is to make task with proper Core installed, so we need to create new file.

.. literalinclude:: django/cmd-1.py
    :language: python
    :caption: bdjango/cmd.py
    :linenos:

And now we can run it:

.. literalinclude:: django/run-6

5.1.3 First real dependency
---------------------------

So now we have a script, which will always run ``python setup.py develop``. But we need to run this only, when setup.py
has changed. That is why we need to change the task implementation.

.. literalinclude:: django/tasks-3.py
    :language: python
    :caption: bdjango/tasks.py
    :linenos:

And also, we need to add some configurations to the core.

.. literalinclude:: django/core-2.py
    :language: python
    :caption: bdjango/core.py
    :linenos:

This time, when we make update and we will not change the ``setup.py`` file, the script will not start the rebuild.
In those scripts we use "bdjango/flags" directory, as a place for storing the flags. You should create a folder before
running the ``beal`` application.

.. literalinclude:: django/run-7

5.1.4 Run Task in chain
-----------------------

If we can create a task for updating the requiretments, why not create a task for creating flags folder? It is very
simple to do that.

.. literalinclude:: django/tasks-4.py
    :language: python
    :caption: bdjango/tasks.py
    :linenos:

``CreateFlagsFolder`` is pretty simple. FileTask has a ``buildf_if(FileDoesNotExists(self.output))`` in the dependency
list, so we do not need to implement it. Also we added 1 more dependency in line 22, which indicates that the
``UpdateRequirements`` task will first run ``CreateFlagsFolder`` and rebuild itself if the ``CreateFlagsFolder`` has
rebuilded.

.. literalinclude:: django/run-8

At this point, we have already created the flags folder by hand, that is why the first run did nothing. But after
removing the folder, the whole chain was rebuilded.
