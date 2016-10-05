Ceagle Portal Configuration
===========================

Placement
---------

config.json should be placed to /etc/ceagle/config.json


Configuration File Description
------------------------------

Configuration file is plain json document with 3 top level keys:

* flask - Flask configuration arguments with Host and Port options added.
* global - All global settings (e.g. cloud portal name)
* cloud_status - cloud_status pages configuration


Configuration Of cloud_status In Nuts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* enabled - If True initialize /cloud_status/ API and "Cloud status" menu
* enabled_dashboards - initializes sub API /cloud_status/availability and /cloud_status/health with sub menus
* regions - list of regions that should be displayed
** region - displayed name of region
** health - dict with 2 items connection URL to Elastic Search &  index from what to query health data production by
            https://github.com/ceagle/health
** availability - dict with single argument "graphite" that is used to specify connection string to graphite that stores metrics.

