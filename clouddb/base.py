# -*- encoding: utf-8 -*-
""" Base object class, basically the same class taken
from jacobian python-cloudservers library"""
import datetime


class Resource(object):
    """ A resource represents a particular instance of an object
    (loadbalancers, protocol, etc). This is pretty much just a bag for
    attributes.  """
    def __init__(self, manager, info):
        self.manager = manager
        self._info = info
        self._add_details(info)

    def _add_details(self, info):
        for (k, v) in info.iteritems():
            setattr(self, k, v)

    def __getattr__(self, k):
        self.get()
        if k not in self.__dict__:
            raise AttributeError("Object has no attribute '%s'" % k)
        else:
            return self.__dict__[k]

    def __repr__(self):
        reprkeys = sorted(k for k in self.__dict__.keys() \
                              if k[0] != '_' and k != 'manager')
        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)

    def get(self):
        new = self.manager.get(self.id)
        self._add_details(new._info)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if hasattr(self, 'id') and hasattr(other, 'id'):
            return self.id == other.id
        return self._info == other._info

    def __setitem__(self, key, value):
        setattr(self, key, value)


class Manager(object):
    """ Managers interact with a particular type of API (loadbalancer,
    protocol, etc.) and provide CRUD operations for them."""
    resource_class = None

    def __init__(self, api):
        self.api = api

    def _list(self, url, response_key):
        resp, body = self.api.client.get(url)
        return [self.resource_class(self, res) for res in body[response_key]]

    def _get(self, url, response_key):
        resp, body = self.api.client.get(url)
        return self.resource_class(self, body[response_key])

    def _create(self, url, body, response_key):
        resp, body = self.api.client.post(url, body=body)
        return self.resource_class(self, body[response_key])

    def _delete(self, url):
        resp, body = self.api.client.delete(url)

    def _update(self, url, body):
        resp, body = self.api.client.put(url, body=body)

    def _restart(self, url, body):
        resp, body = self.api.client.post(url, body=body)

    def _resize(self, url, body):
        resp, body = self.api.client.post(url, body=body)

    def _post(self, url, body):
        resp, body = self.api.client.post(url, body=body)

    def _enable_root(self, url, body, response_key):
        resp, body = self.api.client.post(url, body=body)
        return self.resource_class(self, body[response_key])


class ManagerWithFind(Manager):
    """
    Like a `Manager`, but with additional `find()`/`findall()` methods.
    """
    def find(self, **kwargs):
        """
        Find a single item with attributes matching ``**kwargs``.

        This isn't very efficient: it loads the entire list then filters on
        the Python side.
        """
        rl = self.findall(**kwargs)
        try:
            return rl[0]
        except IndexError:
            #TODO:
            # NotFound(404, "No %s matching %s." %
            # (self.resource_class.__name__, kwargs))
            raise Exception()

    def findall(self, **kwargs):
        """
        Find all items with attributes matching ``**kwargs``.

        This isn't very efficient: it loads the entire list then filters on
        the Python side.
        """
        found = []
        searches = kwargs.items()

        for obj in self.list():
            try:
                if all(getattr(obj, attr) == value \
                           for (attr, value) in searches):
                    found.append(obj)
            except AttributeError:
                continue

        return found


class SubResourceManager(object):
    path = None
    type = None
    resource = None

    def __init__(self, client, dbId=None):
        self.dbId = dbId
        if self.dbId:
            self.dbId = int(self.dbId)
            self.path = "/instances/%s/%s" % (self.dbId, self.type.lower())

        self.client = client

    def get(self):
        ret = self.client.get("%s.json" % self.path)
        tt = ret[1][self.type]
        if tt:
            return self.resource(**(tt))

    def add(self, ssp):
        dico = ssp.toDict()
        ret = self.client.put(self.path, body={self.type: dico})
        return ret

    def delete(self):
        ret = self.client.delete(self.path)
        return ret

    def restart(self):
        ret = self.client.post(self.path)
        return ret

    def resize(self):
        ret = self.client.post(self.path)
        return ret


class SubResource(object):
    def toDict(self, includeNone=False):
        """
        Convert the local attributes to a dict
        """
        ret = {}
        for attr in self.__dict__:
            if self.__dict__[attr] is None and not includeNone:
                continue
            if not attr.startswith("_"):
                ret[attr] = self.__dict__[attr]
        return ret

    def __setitem__(self, key, value):
        setattr(self, key, value)


class SubResourceDict(object):
    def __init__(self, dico):
        self.dico = dico

    def __iter__(self):
        for d in self.dico:
            yield d

    def __getitem__(self, i):
        return self.dico[i]

    def __len__(self):
        return len(self.dico)

    #Trying hard to look like a dict.. Not sure if I should do that.
    def __repr__(self):
        ret = '['
        for d in self.dico:
            ret += str(d)
            ret += ", "
        ret = ret[0:-2] + "]"
        return ret


def getid(obj):
    """
    Abstracts the common pattern of allowing both an object or an object's ID
    (integer) as a parameter when dealing with relationships.
    """
    try:
        return obj.id
    except AttributeError:
        # return int(obj)
        return obj


def convert_iso_datetime(dt):
    """
    Convert iso8601 to datetime
    """
    isoFormat = "%Y-%m-%dT%H:%M:%S+0000"
    if type(dt) is datetime.datetime:
        return dt

    if dt.endswith("Z"):
        dt = dt.split('Z')[0]
        isoFormat = "%Y-%m-%dT%H:%M:%S"

    return datetime.datetime.strptime(dt, isoFormat)
