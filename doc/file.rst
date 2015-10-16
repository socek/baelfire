2.2 File Tasks
==============

2.2.1 File Task
---------------

Task class can be enhanced to your own needs, but in most cases we want file
related tasks, for example "change if something chanded", or "create" file if
not exists.

.. literalinclude:: code/doc5.py
    :language: python
    :caption: doc5.py
    :linenos:

.. code-block:: bash

    $ python doc5.py
     * DEBUG __main__.FirstTask: Dependency baelfire.dependencies.file.FileDoesNotExists result: True *
     * DEBUG __main__.FirstTask: Need to run: True *
     * DEBUG __main__.ParentTask: Dependency baelfire.dependencies.task.RunBefore result: False *
     * DEBUG __main__.SecondTask: Dependency baelfire.dependencies.file.FileDoesNotExists result: True *
     * DEBUG __main__.SecondTask: Need to run: True *
     * DEBUG __main__.ParentTask: Dependency baelfire.dependencies.task.RunBefore result: False *
     * DEBUG __main__.ParentTask: Need to run: False *
     * INFO __main__.FirstTask: Running *
     * INFO __main__.SecondTask: Running *

FileTask has already added FileDoesNotExists dependency for output file. This
file can be configured by 2 ways: setting ``output`` with direct url to a file
or setting ``output_name`` which is a key used in ``Task.paths``, so the path
can be change in the future.

2.2.2 Template Task
-------------------

Template task is used to create a file from template. We use
`Jinja2 <http://jinja.pocoo.org/>`_ for template system.

.. literalinclude:: code/doc6.py
    :language: python
    :caption: doc6.py
    :linenos:

.. code-block:: bash

    $ python doc6.py
    $ cat source.txt
    {{paths['source']}}
    {{paths['output']}}
    $ cat output.txt
    source.txt
    output.txt

We created 2 tasks. First to create the template and second to create a file
from template. For default for context we only gave settings and paths. If
we want to add something to context just ovveride ``generate_context`` method:

.. literalinclude:: code/doc7.py
    :language: python
    :caption: doc7.py
    :linenos:

.. code-block:: bash

    $ python doc7.py
    $ cat source.txt
    {{paths['source']}}
    {{paths['output']}}
    {{myvar}}
    $ cat output.txt
    source.txt
    output.txt
    my var 10
