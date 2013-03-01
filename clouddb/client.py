import httplib2
import os
import sys
import json
import pprint
import time

import clouddb.consts
import clouddb.errors


class CloudDBClient (httplib2.Http):
    def __init__(self, username, api_key, region, auth_url=None):
        super(CloudDBClient, self).__init__()
        self.username = username
        self.api_key = api_key

        if not auth_url and region == "lon":
            auth_url = clouddb.consts.UK_AUTH_SERVER
        else:
            auth_url = clouddb.consts.DEFAULT_AUTH_SERVER

        self.auth_url = auth_url

        if region.lower() in clouddb.consts.REGION.values():
            self.region = region
        elif region.lower() in clouddb.consts.REGION.keys():
            self.region = clouddb.consts.REGION[region]
        else:
            raise clouddb.errors.InvalidRegion()

        self.auth_token = None
        self.account_number = None
        self.region_account_url = None

    def authenticate(self):
        headers = {'Content-Type': 'application/json'}
        body = '{"credentials": {"username": "%s", "key": "%s"} }' % (
                   self.username, self.api_key)
        response, body = self.request(self.auth_url, 'POST', body=body,
                                      headers=headers)

        auth_data = json.loads(body)['auth']

        if response.status == 401:
            raise clouddb.errors.AuthenticationFailed()

        if response.status != 200:
            raise clouddb.errors.ResponseError(response.status,
                                               response.reason)

        self.account_number = int(os.path.basename(
            auth_data['serviceCatalog']['cloudServers'][0]['publicURL']))
        self.auth_token = auth_data['token']['id']

        self.region_account_url = "%s/%s" % (
            clouddb.consts.REGION_URL % (self.region),
            self.account_number)

    def _clouddb_request(self, url, method, **kwargs):
        if not self.region_account_url:
            self.authenticate()

        kwargs.setdefault('headers', {})['X-Auth-Token'] = self.auth_token
        kwargs['headers']['User-Agent'] = clouddb.consts.USER_AGENT
        kwargs['headers']['Accept'] = 'application/json'
        if 'body' in kwargs:
            kwargs['headers']['Content-Type'] = 'application/json'
            kwargs['body'] = json.dumps(kwargs['body'])

        ext = ""
        fullurl = "%s%s%s" % (self.region_account_url, url, ext)

        #DEBUGGING:
        if 'PYTHON_CLOUDDB_DEBUG' in os.environ:
            pp = pprint.PrettyPrinter(stream=sys.stderr, indent=2)
            sys.stderr.write("URL: %s\n" % (fullurl))
            sys.stderr.write("ARGS: %s\n" % (str(kwargs)))
            sys.stderr.write("METHOD: %s\n" % (str(method)))
            if 'body' in kwargs:
                pp.pprint(json.loads(kwargs['body']))

        response, body = self.request(fullurl, method, **kwargs)

        if 'PYTHON_CLOUDDB_DEBUG' in os.environ:
            pp = pprint.PrettyPrinter(stream=sys.stderr, indent=2)
            sys.stderr.write('RESPONSE:')
            pp.pprint(response)

        if body:
            try:
                body = json.loads(body)
            except(ValueError):
                pass

        if (response.status < 200) or (response.status > 299):
            raise clouddb.errors.ResponseError(response.status,
                                               response.reason)

        return response, body

    def put(self, url, **kwargs):
        return self._clouddb_request(url, 'PUT', **kwargs)

    def get(self, url, **kwargs):
        return self._clouddb_request(url, 'GET', **kwargs)

    def post(self, url, **kwargs):
        return self._clouddb_request(url, 'POST', **kwargs)

    def delete(self, url, **kwargs):
        return self._clouddb_request(url, 'DELETE', **kwargs)
