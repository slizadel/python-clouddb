==================================================================
 Python interface to Rackspace Cloud Databases
==================================================================

:Homepage:  https://github./slizadel/python-clouddb
:Credits:   Copyright 2012 Slade Cozart <slade.cozart@gmail.com>
:Add'l Credits:  Chmouel Boudjnah <chmouel@chmouel.com> for his work on python-cloudlb
:Licence:   BSD
:API Reference: http://docs.rackspace.com/cdb/api/v1.0/cdb-devguide/content/overview.html


Usage
=====

List all instances and databases::

  #!/usr/bin/env python
  import clouddb
  cdb = clouddb.CloudDB('username', 'apikey', 'region')
  for instance in cdb.get_instances():
      print '%s - %s Flavor %s Size %s' % (instance.id, instance.name, 
                                           instance.flavor['id'], 
                                           instance.volume['size'])
      for database in instance.get_databases():
          print '    ', database.name

Get an instance by id::

  #!/usr/bin/env python
  import clouddb
  cdb = clouddb.CloudDB('username', 'apikey', 'region')
  instance = cdb.get_instance('da3d55cc-7998-4ef6-9375-d8d7ee0d469a')
  print instance.name

Delete an instance by id::

  #!/usr/bin/env python
  import clouddb
  cdb = clouddb.CloudDB('username', 'apikey', 'region')
  cdb.delete_instance('da3d55cc-7998-4ef6-9375-d8d7ee0d469a')

Create instance with no databases::

  #!/usr/bin/env python
  import clouddb
  cdb = clouddb.CloudDB('username', 'apikey', 'region')
  instance = cdb.create_instance('myinstance', 1, 1)

Create instance with two databases::

  #!/usr/bin/env python
  import clouddb
  cdb = clouddb.CloudDB('username', 'apikey', 'region')

  databases=[{'name': 'db1'}, 
             {'name': 'db2', 'character_set': 'latin5', 'collate': 'latin5_turkish_ci'}]
  instance = cdb.create_instance('myinstance', 1, 1, databases=databases)

Create database in existing instance::

  #!/usr/bin/env python
  import clouddb
  cdb = clouddb.CloudDB('username', 'apikey', 'region')
  database=[{'name':'new_database'}]
  instance = cdb.get_instance('da3d55cc-7998-4ef6-9375-d8d7ee0d469a')
  instance.create_databases(databases)

Create user for database::

  #!/usr/bin/env python
  import clouddb
  cdb = clouddb.CloudDB('username', 'apikey', 'region')
  instance = cdb.get_instance('instanceid')
  instance.create_user('username', 'password', ['db1', 'db2'])
