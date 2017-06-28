2.2 Core model
==============

2.2.1 Core settings
-------------------

Baelfire use `MorfDict <https://pythonhosted.org/MorfDict/>`_'s ``StringDict`` for settings and ``PathDict`` for path
configuration. All linked tasks have the same settings and paths object, so we can edit in the parent task if we want,
but this is not recomended. Better way is to make all the configuration in the Core object.

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

2.2.2 Saving and loading settings
---------------------------------

Sometimes we would like to save settings, so it can be retrived from disk. For example, the name of the project we need
only at the start and we can retrive it from disk next time, but the rest of the configuration can be stored in python
code.

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


2.2.2 Task replacment
---------------------
