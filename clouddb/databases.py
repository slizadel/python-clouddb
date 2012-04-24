# -*- encoding: utf-8 -*-
#from clouddb.base import SubResource, SubResourceDict
from clouddb import base


class Database(base.Resource):
    def __repr__(self):
        return "<Database: %s>" % (self.name)


class DatabaseManager(base.ManagerWithFind):
    resource_class = Database

    def get_databases(self, instanceid):
        return [x for x in self._list("/instances/%s/databases" % (
                                      instanceid), "databases")]
