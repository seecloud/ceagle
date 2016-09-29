Cloud Eagle is support portal for OpenStack
===========================================

Cloud Eagle is DevOps portal that simplifies operating cloud, it covers next topics:

* Hardware & virtual inventory
* Capacity management
* Janitor monkey
* Configuration tracker
* Security audit
* High level cloud status dashboard
* Logging, Monitoring, Alerting (ELK)
* Synthetic tests for measuring key API performance
* Synthetic tests for measuring network bandwidth/latency
* API request tracing


Running As A Docker Container
-----------------------------

Build Docker Container
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

    docker build -t ceagle:latest .


Configure & Run Container
~~~~~~~~~~~~~~~~~~~~~~~~~

First of all create config file, for example in:

.. code-block:: sh

    mkdir ~/ceagle-conf
    vi ~/ceagle-conf/conf.cfg
    # Provide Flask conf options:
    # http://flask.pocoo.org/docs/0.11/config/#builtin-configuration-values


Run you container with volume that contains config

.. code-block:: sh

    docker run -d --name ceagle -v ~/ceagle-conf:/etc/ceagle -p  5000:5000 ceagle
