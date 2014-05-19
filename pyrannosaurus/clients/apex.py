import string
import sys
import os.path

from suds.client import Client
from suds.cache import FileCache

from pyrannosaurus import get_package_dir
from pyrannosaurus.clients.base import BaseClient
    
class ApexClient(BaseClient):
    _debug_levels = ['Db', 'Workflow', 'Validation', 'Callout', 'Apex_code', 'Apex_profiling']
    
    def __init__(self, wsdl='wsdl/apex.xml', cacheDuration=0, **kwargs):
        super(ApexClient, self).__init__()
        #TODO: clean this up
        wsdl = get_package_dir(wsdl)
        wsdl = 'file:///' + os.path.abspath(wsdl)

        if cacheDuration > 0:
            cache = FileCache()
            cache.setduration(seconds = cacheDuration)
        else:
            cache = None   

        self._client = Client(wsdl, cache = cache)

        headers = {'User-Agent': 'Salesforce/' + self._product + '/' + '.'.join(str(x) for x in self._version)}
        self._client.set_options(headers = headers)

    def login(self, username, password, token='', is_production=False):
        lr = super(ApexClient, self)._login(username, password, token, is_production)
        #replace the metadata 'm' with the apex 's'
        url = lr.metadataServerUrl.replace('/m/', '/s/')
        self._setEndpoint(url)
        super(ApexClient, self)._setEndpoint(lr.serverUrl, base=True)
        super(ApexClient, self).setSessionHeader(self._sessionHeader)
        return lr

    def run_tests(self, classes=None, namespace=None, all_tests=False):
        self._setHeaders('runTests')
        run_tests_request = self._client.factory.create('RunTestsRequest')
        if not classes:
            all_tests = True
            classes = []

        run_tests_request.allTests = all_tests
        run_tests_request.classes = classes
        run_tests_request.namespace = namespace
        run_tests_request.packages = None

        run_tests_response = self._client.service.runTests(run_tests_request)

        return run_tests_response

    def execute_anonymous(self, apex):
        self._setHeaders('executeAnonymous')
        execute_anonymous_response = self._client.service.executeAnonymous(apex)

        return execute_anonymous_response

    def set_timeout(self, time):
        self._client.set_options(timeout=time)
