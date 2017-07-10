2.3 File Tasks
==============

2.3.1 File Task
---------------

Task class can be extended to your own needs, but in most cases we want file related tasks, for example "build file if
other file has rebuilded", or "create file if not exists". For this purpose Baelfire comes with FileTask.

.. literalinclude:: code/doc5.py
    :language: python
    :caption: doc5.py
    :linenos:

.. code-block:: bash

    $ python doc5.py
     * DEBUG __main__.FirstTask: Dependency baelfire.dependencies.file.FileDoesNotExists result: True *
     * DEBUG __main__.FirstTask: Need to run: True *
     * DEBUG __main__.ParentTask: Dependency baelfire.dependencies.task.RunTask result: False *
     * DEBUG __main__.SecondTask: Dependency baelfire.dependencies.file.FileDoesNotExists result: True *
     * DEBUG __main__.SecondTask: Need to run: True *
     * DEBUG __main__.ParentTask: Dependency baelfire.dependencies.task.RunTask result: False *
     * DEBUG __main__.ParentTask: Need to run: False *
     * INFO __main__.FirstTask: Running *
     * INFO __main__.SecondTask: Running *

FileTask has a default FileDoesNotExists dependency for output file. Path for the output file can be configured by
reimplementing output property (direct path to task) or reimplementing output_name property (key used for .paths in
Core).

2.3.2 Template Task
-------------------

Template task is used to create a file from template. We use `Jinja2 <http://jinja.pocoo.org/>`_ for template system.

.. literalinclude:: code/doc6.py
    :language: python
    :caption: doc6.py
    :linenos:

.. code-block:: bash

    $ python doc6.py
    $ cat source.txt
    {{paths.get('source')}}
    {{paths.get('output')}}
    {{my_context}}
    $ cat output.txt
    /home/socek/projects/baelfire/doc/code/source.txt
    /home/socek/projects/baelfire/doc/code/output.txt
    this is my context


We created 2 tasks. First to create the template and second to create a file from template. Default context has settings
and paths in it. If we want to add something to context just ovveride ``generate_context`` method:

.. literalinclude:: code/doc7.py
    :language: python
    :caption: doc7.py
    :linenos:

.. code-block:: bash

    $ python doc7.py
    $ cat source2.txt
    {{paths.get('source')}}
    {{paths.get('output')}}
    {{myvar}}
    $ cat output2.txt
    /home/socek/projects/baelfire/doc/code/source2.txt
    /home/socek/projects/baelfire/doc/code/output2.txt
    my var 10

