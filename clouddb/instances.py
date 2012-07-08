from clouddb import base


class Instance(base.Resource):
    def __repr__(self):
        return "<Instance: %s : %s>" % (self.name, self.id)

    def delete(self):
        self.manager.delete(self)

    def restart(self):
        self.manager.restart(self)

    def resize(self, size):
        self.manager.resize(self, size)

    def get_databases(self):
        return self.manager.get_databases(self)

    def create_databases(self, databases):
        return self.manager.create_databases(self, databases)

    def delete_database(self, database):
        return self.manager.delete_database(self, database)

    def enable_root(self):
        resp = self.manager._enable_root("/instances/%s/root" % self.id, '',
                                         "user")
        return resp.password

    def check_root(self):
        resp = self.manager.api.client.get("/instances/%s/root" % self.id)
        return resp[1]["rootEnabled"]

    def create_user(self, username, password, databases):
        return self.manager.create_user(self, username, password, databases)

    def list_users(self):
        return self.manager.list_users(self)

    def delete_user(self, user):
        return self.manager.delete_user(self, user)


class InstanceManager(base.ManagerWithFind):
    resource_class = Instance

    def get_instance(self, instanceid):
        return self._get("/instances/%s" % \
                         base.getid(instanceid), "instance")

    def get_instances(self):
        return [x for x in self._list("/instances", "instances")
                   if x._info['status'] != "DELETED"]

    def create_instance(self, name, flavor=1, volume=1, databases=[]):
        flavorref = '%s/flavors/%d' % (
                      self.api.client.region_account_url,
                      flavor)
        body = {'instance': {
                     'name': name,
                     'flavorRef': flavorref,
                     'databases': databases,
                     'volume': {'size': volume}}}
        return self._create("/instances", body, "instance")

    def delete_instance(self, instanceid):
        self.api.client.authenticate()
        self._delete("/instances/%s" % base.getid(instanceid))

    def restart_instance(self, instanceid):
        body = {"restart": {}}
        self._restart("/instances/%s/action" % base.getid(instanceid), body)

    def resize_instance(self, instanceid, size):
        body = {"resize": {"volume": {"size": size}}}
        self._resize("/instances/%s/action" % base.getid(instanceid), body)

    """ Database Operations """
    def get_databases(self, instance):
        return self.api.databases.get_databases(base.getid(instance))

    def create_databases(self, instance, databases):
        body = {"databases": databases}
        return self._post("/instances/%s/databases" % base.getid(instance),
                          body)

    def delete_database(self, instance, databasename):
        self._delete("/instances/%s/databases/%s" % (instance.id,
                                                     databasename))

    """ User Operations """

    def list_users(self, instance):
        return self.api.users.list(base.getid(instance))

    def create_user(self, instance, username, password, databases):
        return self.api.users.create(base.getid(instance), username, password,
                                     databases)

    def delete_user(self, instance, username):
        return self.api.users.delete(base.getid(instance), username)
