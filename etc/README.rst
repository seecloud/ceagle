Ceagle Portal Configuration
===========================

Placement
---------

Configuration file should be placed to */etc/ceagle/config.json*.

If there is an environment variable *CEAGLE_CONF* set, it is used as priority.
In this case it is important to use absolute path to configuration file.

Example:

.. code-block::

    export CEAGLE_CONF=/home/username/configs/custom_config.json
    ./runserver.sh

Configuration File Description
------------------------------

Configuration file is plain JSON document with top level keys
that describes Flask and available microservices configuration:

Here is a simple example with configuration for Flask and two microservices:

.. code-block::

  {
    "flask": {
        "PORT": 5001,
        "HOST": "0.0.0.0",
        "DEBUG": true
    },
    "cloud_status": {
        "endpoint": "http://dummy.example.org/api/cloud_status"
    },
    "capacity": {
        "endpoint": "http://dummy.example.org/api/capacity"
    }
  }

Flask configuration
~~~~~~~~~~~~~~~~~~~

Flask configuration is set via *flask* key and described in
`official documentation <http://flask.pocoo.org/docs/0.11/config/>`_.

The only extra options are HOST and PORT.


Microservices configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The only mandatory parameter is *endpoint*,
which defines microservice endpoint URL

There are no limitations for other parameters.
