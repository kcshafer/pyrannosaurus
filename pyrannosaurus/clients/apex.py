import string
import sys
import os.path

from suds.client import Client
from suds.cache import FileCache

from pyrannosaurus.clients.base import BaseClient
    
class ApexClient(BaseClient):
    _debug_levels = ['Db', 'Workflow', 'Validation', 'Callout', 'Apex_code', 'Apex_profiling']
    
    def __init__(self, wsdl='wsdl/apex.xml', cacheDuration=0, **kwargs):
        super(ApexClient, self).__init__()
        #TODO: clean this up
        if '://' not in wsdl:
            if os.path.isfile(wsdl):
                wsdl = 'file://' + os.path.abspath(wsdl)

        if cacheDuration > 0:
            cache = FileCache()
            cache.setduration(seconds = cacheDuration)
        else:
            cache = None
        print wsdl
        self._client = Client(wsdl, cache = cache)

        headers = {'User-Agent': 'Salesforce/' + self._product + '/' + '.'.join(str(x) for x in self._version)}
        self._client.set_options(headers = headers)

    #TODO : this really won't work, needs check for sobjecttype to go to right client
    def generateHeader(self, sObjectType):
        try:
          return self._client.factory.create(sObjectType)
        except:
          print 'There is not a SOAP header of type %s' % sObjectType
    
    def _default_log_info(self):
        log_info = self._client.factory.create('LogInfo')
        log_info.category = 'All'
        log_info.level = 'Debug'
        return log_info

    #TODO eval
    def _setHeaders(self, call = None):
        headers = {'SessionHeader': self._sessionHeader}
        print self._sessionHeader
        if(call == 'runTests'):
            debug_header = self.generateHeader('DebuggingHeader')
            print debug_header
            debug_header.categories.append(self._default_log_info())  
        self._client.set_options(soapheaders = headers)

    def login(self, username, password, token=''):
        lr = super(ApexClient, self)._login(username, password, token)
        self._setEndpoint("https://cs18.salesforce.com/services/Soap/s/29.0")

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