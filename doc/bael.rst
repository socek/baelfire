3 Bael - command line
=====================

3.1 About
---------

There is no need to create your own command lines just to run tasks. Baelfire comes with command line task runner.
It is called ``bael``.

3.2 Help
--------

.. code-block:: bash

    usage: bael [-h] [-t TASK] [-g] [-r GRAPH_FILE]
            [-l {debug,info,warning,error,critical}]

    optional arguments:
      -h, --help            show this help message and exit

    Tasks:
      Tasks related options

      -t TASK, --task TASK  Run this task.
      -g, --graph           Draw task dependency graph.

    Other:
      Other useful options

      -r GRAPH_FILE, --graph-file GRAPH_FILE
                            Draw graph from report file.

    Logging::
      Logging related options.

      -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                            Log level
    (venv_baelfire)socek:~/projects/baelfire (master ✗) $ bael
    usage: bael [-h] [-t TASK] [-g] [-r GRAPH_FILE]
                [-l {debug,info,warning,error,critical}]

    optional arguments:
      -h, --help            show this help message and exit

    Tasks:
      Tasks related options

      -t TASK, --task TASK  Run this task.
      -g, --graph           Draw task dependency graph.

    Other:
      Other useful options

      -r GRAPH_FILE, --graph-file GRAPH_FILE
                            Draw graph from report file.

    Logging::
      Logging related options.

      -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                            Log level

3.3 Running tasks
-----------------

.. code-block:: bash

    bael -t some.lib:TaskClass

``-t`` switch is expecting python dotted url for Task class or function which will return created Task object. Module with
tasks should be in python path. All tasks runned by bael will generate .baelfire.report file which is a yaml file with
report of what has been runned and why.

.. literalinclude:: code/doc12.py
    :language: python
    :caption: doc12.py
    :linenos:

.. code-block:: bash

    $ bael -t doc12:run
     * INFO doc12.MyTask: Running *
    hello

3.4 Graphs
----------

``bael`` can create graph from report created from last run. This is very helpful, when you want to debug your tasks.

.. code-block:: bash

    $ bael -t doc12:run -g

If you forgot the switch, after running task you can generate graph from report
file.

.. code-block:: bash

    $ bael -r .baelfire.report

Graphs are generated in ``graph.png`` file. If you would like to use the graph in your code, you should check
``baelfire.application.commands.graph.graph:Graph``.
