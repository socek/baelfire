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
running the ``bael`` application.

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
rebuild.

.. literalinclude:: django/run-8

At this point, we have already created the flags folder by hand, that is why the first run did nothing. But after
removing the folder, the whole chain was rebuild.

Most of the Python projects use requiretments.txt file instead of setup.py. In our sample project we will use both, just
for the sake of creating Baelfire tasks.

.. literalinclude:: django/tasks-5.py
    :language: python
    :caption: bdjango/tasks.py
    :linenos:

Our goal is to update ``setup.py develop`` and ``requiretments.txt`` in different tasks. I did not wanted to change
``cmd.py`` file, so I moved what we had in ``UpdateRequirements`` into ``SetupPyDevelop`` and created base class
``BaseRequirements`` in order to not repeat the same code for ``UpdateRequirementsProduction``. ``UpdateRequirements``
was created to link those two tasks, but it does not need to build anything.

.. image:: ../images/graph_doc514_a.png
    :alt: Tasks

Some changes needs to be done in the core file as well. Also, we have a new file: ``requiretments.txt``

.. literalinclude:: django/core-3.py
    :language: python
    :caption: bdjango/core.py
    :linenos:

.. literalinclude:: django/req-1.txt
    :caption: requirements.txt
    :linenos:

So now we can run our newly created baelfire tasks.

.. literalinclude:: django/run-9

5.1.5 Runserver
---------------

Main purpose of the Baelfire in our sample project is to start runserver with all it's dependencies. For now, we have
implemented dependency of updating packages to proper version. It is enough to implement a task for starting the
developer's server.

.. literalinclude:: django/tasks-6.py
    :language: python
    :caption: bdjango/tasks.py
    :linenos:

The ``StartRunserver`` task has been implemented. In line 75 we added ``AlwaysTrue`` dependency which will result in
rebuilding this task every time it will be started no matter every other dependency.

Now we need to implement endpoint for starting new task.

.. literalinclude:: django/cmd-2.py
    :language: python
    :caption: bdjango/cmd.py
    :linenos:

No new settings needs to be done, so we will just test the run.

.. literalinclude:: django/run-10

As you can see on the listing above, starting the runserver will first reinstall requiretments before starting the
server.

5.1.6 Migrations
----------------

You probably noticed that runserver is yelling at us (color of the message is red, which means yelling!), that we did
not made migrations.

.. literalinclude:: django/tasks-7.py
    :language: python
    :caption: bdjango/tasks.py
    :linenos:

Now we have 2 tasks which needs to use ``manage.py``, so I made base class ``BaseManagePy`` with default dependency,
which make sure that the requiretments will be updated before running ``manage.py`` command. At this point we may want
to add ``AlwaysTrue`` dependency here, but it is design flaw. In the future, you may want to use ``manage.py`` command
which does not need to be rebuild every time it will be started.

.. literalinclude:: django/run-11

Now, every time we will start runserver, we will run migrations before.

.. image:: ../images/graph_doc516_a.png
    :alt: Tasks

As you can see, we are using UpdateRequirements in two places, but the Baelfire does not complain.
