from clouddb.client import CloudDBClient
from clouddb.databases import DatabaseManager
from clouddb.instances import InstanceManager
from clouddb.flavors import FlavorManager
from clouddb.users import UserManager
import pprint
from clouddb.consts import VERSION
__version__ = VERSION


class CloudDB(object):
    """
    Top-level object to access the Rackspace Cloud Load Balancer API.

    TODO:
    """

    def __init__(self, username, api_key, region, **kwargs):
        self.client = CloudDBClient(username, api_key, region, **kwargs)
        self.databases = DatabaseManager(self)
        self.instances = InstanceManager(self)
        self.flavors = FlavorManager(self)
        self.users = UserManager(self)

    def get_usage(self, startTime=None, endTime=None):
        startTime = startTime and startTime.isoformat()
        endTime = endTime and endTime.isoformat()
        ret = get_usage(self.client, startTime=startTime, endTime=endTime)
        return ret

    def get_algorithms(self):
        g = self.client.get("/instances/algorithms")[1]['algorithms']
        return [x['name'] for x in g]

    def get_protocols(self):
        g = self.client.get("/instances/protocols")[1]['protocols']
        return [x['name'] for x in g]

    def authenticate(self):
        """
        Authenticate against the server.

        Normally this is called automatically when you first
        access the API, but you can call this method to force
        authentication right now.

        Returns on success; raises :exc:`TODO:` if the credentials
        are wrong.
        """
        self.client.authenticate()

    def get_instances(self):
        return self.instances.get_instances()

    def get_instance(self, instanceid):
        return self.instances.get_instance(instanceid)

    def get_instances_details(self):
        return self.instances.get_instances_details()

    def delete_instance(self, instanceid):
        self.instances.delete_instance(instanceid)

    def restart_instance(self, instanceid):
        self.instances.restart_instance(instanceid)

    def resize_instance(self, instanceid, size):
        self.instances.resize_instance(instanceid, size)

    def create_instance(self, name, flavor=1, volume=1, databases=[]):
        return self.instances.create_instance(name, flavor, volume, databases)

    def get_instance_status(self):
        return self.instances.get_instance_status()

    def create_database(self, instanceid, databases):
        return self.instances.create_database(instanceid, databases)

    def get_instance_databases(self, instanceid):
        return self.instances.get_instance_databases(instanceid)

    def delete_database(self, instanceid, databasename):
        self.instances.delete_database(instanceid, databasename)

    # Flavor functionality
    def list_flavors(self):
        return self.flavors.list_flavors()

    def get_flavor(self, flavorid):
        return self.flavors.get_flavor(flavorid)

    # Root Functionality
    def enable_root(self):
        return self.instances.enable_root()

    def check_root(self, instanceid):
        return self.instances.check_root(instanceid)

    # User Functionality
    # def create_user(self, instanceid, users):
    #	return self.instances.create_user(instanceid, users)

    def list_users(self, instanceid):
        return self.users.list_users(instanceid)

    def delete_user(self, instanceid, username):
        self.users.delete_user(instanceid, username)
