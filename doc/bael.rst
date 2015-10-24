3 Bael - command line
=====================

3.1 About
---------

There is no need to create your own command lines just to run tasks. We created
command line named "bael"

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

    bael -t some.lib.TaskClass

All tasks runned by bael will generate .baelfire.report file which is a yaml
file with report of what has been runned and why.

3.4 Graphs
----------

There is a possibility to generate graph from task run. Just after task add "-g"
switch.

.. code-block:: bash

    $ bael -t tester.taskme3:Example -g

If you forgot the switch, after running task you can generate graph from report
file.

.. code-block:: bash

    $ bael -r .baelfire.report

Graphs are generated in ``graph.png`` file.
