2.3 SubProcessing
=================

2.3.1 SubprocessTask
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

All args from ``SubprocessTask.popen`` is passed to ``subprocess.Popen``, but
the ``shell`` argument is from default set to ``True``. If you want to change
that just override ``_set_default_args`` method.

.. literalinclude:: code/doc8.py
    :language: python
    :caption: doc9.py
    :linenos:

.. code-block:: bash

    $ python doc9.py
    something

2.3.2 Pid dependecies
---------------------
