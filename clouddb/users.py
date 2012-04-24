# -*- encoding: utf-8 -*-
#from clouddb.base import SubResource, SubResourceDict
from clouddb import base


class User(base.Resource):
    def __repr__(self):
        return "<User: %s>" % (self.name)


class UserManager(base.ManagerWithFind):
    resource_class = User

    def create(self, instanceid, username, password, databases):
        dbs = []
        for database in databases:
            dbs.append({'name': database})
        body = {'users': [{'name': username, 'password': password, 'databases': dbs}]}
        return self._post("/instances/%s/users" % instanceid, body)

    def delete(self, instanceid, username):
        self._delete("/instances/%s/users/%s" % (
                     base.getid(instanceid), username))

    def list(self, instanceid):
        return [x for x in self._list("/instances/%s/users" % instanceid,
                                      "users")]
