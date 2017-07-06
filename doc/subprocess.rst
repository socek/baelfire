2.4 SubProcessing
=================

2.4.1 SubprocessTask
--------------------
SubprocessTask is a way to run external programs. It is just a wrapper for
``subprocess.Popen``.

.. literalinclude:: code/doc8.py
    :language: python
    :caption: doc8.py
    :linenos:

.. code-block:: bash

    $ python doc8.py
    something

All args from ``SubprocessTask.popen`` is passed to ``subprocess.Popen``, but the ``shell`` argument is from default,
which is set to ``True``. If you want to change that, just override ``_set_default_args`` method.

.. literalinclude:: code/doc9.py
    :language: python
    :caption: doc9.py
    :linenos:

.. code-block:: bash

    $ python doc9.py
    something

2.4.2 Pid dependencies
----------------------
``baelfire.dependencies.pid.PidIsRunning`` and ``baelfire.dependencies.pid.PidIsNotRunning``
are dependencies which are designed to work with pid numbers. PidIsRunning will
indicate build if pid is already running. PidIsNotRunning will only trigger build
if pid is not running. ``PidIsRunning`` and ``PidIsNotRunning`` init method will
accept pid in 3 ways:

* pid - as a raw number
* pid_file_name - pid file name from .paths
* pid_file_path - raw pif file path

.. literalinclude:: code/doc10.py
    :language: python
    :caption: doc10.py
    :linenos:

.. code-block:: bash

    $ python doc10.py
    sleep is still running...
    - After Termination
    sleep is not running!

2.4.3 Ignore abort error
------------------------

``SubprocessTask`` has a setting named IGNORE_ABORT which will change behaviour of the error mechanism. When this var is
set to True (default) and the task will be aborted (for example, by using CTRL+C), then no exception will be raised and
the command will just be ended. But if we set this to False, then the command will raise a CommandAbort error.

.. literalinclude:: code/doc15.py
    :language: python
    :caption: doc15.py
    :linenos:
