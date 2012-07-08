from clouddb import base


class Flavor(base.Resource):
    def __repr__(self):
        return "<Flavor: %s>" % self.name


class FlavorManager(base.ManagerWithFind):
    resource_class = Flavor

    def list_flavors(self):
        return [x for x in self._list("/flavors", "flavors")]

    def get_flavor(self, flavorid):
        return self._get("/flavors/%s" % base.getid(flavorid), "flavor")
