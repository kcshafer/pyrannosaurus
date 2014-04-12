import string
import sys
import os.path

from suds.client import Client
from suds.cache import FileCache 

from pyrannosaurus.utils import package_to_dict, zip_to_fs

class MetadataClient(object):
    _sessionHeader = None
    _product = 'Metadata Tool'
    _version = (0, 0, 0)
    _location = None 

    _loginScopeHeader = None

    def __init__(self, wsdl, cacheDuration = 0, **kwargs):
        if '://' not in wsdl:
            if os.path.isfile(wsdl):
                wsdl = 'file://' + os.path.abspath(wsdl)

        if cacheDuration > 0:
            cache = FileCache()
            cache.setduration(seconds = cacheDuration)
        else:
            cache = None

        self._meta_client = Client(wsdl, cache = cache)

        headers = {'User-Agent': 'Salesforce/' + self._product + '/' + '.'.join(str(x) for x in self._version)}
        self._meta_client.set_options(headers = headers)

        login_wsdl = 'wsdl/partner.xml'
        if '://' not in login_wsdl:
            if os.path.isfile(login_wsdl):
                login_wsdl = 'file://' + os.path.abspath(login_wsdl)
        self._login_client = Client(login_wsdl, cache = cache)

    #TODO eval 
    def generateHeader(self, sObjectType):
        try:
          return self._meta_client.factory.create(sObjectType)
        except:
          print 'There is not a SOAP header of type %s' % sObjectType
    
    #TODO eval
    def _setEndpoint(self, location):
        try:
          self._meta_client.set_options(location = location)
        except:
          self._meta_client.wsdl.service.setlocation(location)

        self._location = location

    #TODO eval 
    def _setHeaders(self, call = None):
        headers = {'SessionHeader': self._sessionHeader}

        if call == 'login':
            if self._loginScopeHeader is not None:
                headers['LoginScopeHeader'] = self._loginScopeHeader
            self._login_client.set_options(soapheaders = headers)

        self._meta_client.set_options(soapheaders = headers)

    #TODO: replace
    def setLoginScopeHeader(self, header):
        self._loginScopeHeader = header

    #TODO: replace
    def setSessionHeader(self, header):
        self._sessionHeader = header

    def login(self, username, password):
        self._setHeaders('login')
        result = self._login_client.service.login(username, password)

        header = self.generateHeader('SessionHeader')
        header.sessionId = result['sessionId']
        self.setSessionHeader(header)
        self._sessionId = result['sessionId']

        self._setEndpoint(result['metadataServerUrl'])

        return result

    def deploy(self):
        self._setHeaders('deploy')
        obj = self._meta_client.factory.create('ListMetadataQuery')
        obj.type = 'CustomObject'
        args = []
        args.append(obj)
        result = self._meta_client.service.listMetadata(args, 20.0)

        return result

    def retrieve(self, package_manifest, api_version=29.0, api_access='Unrestricted', singlePackage=True):
        self._setHeaders('retrieve')
        retrieve_request = self._meta_client.factory.create('RetrieveRequest')
        retrieve_request.apiVersion = api_version
        retrieve_request.singlePackage = singlePackage
        retrieve_request.unpackaged.apiAccessLevel.value = api_access
        package_dict = package_to_dict(package_manifest)

        for name,members in package_dict.iteritems():
            pkg_mem = self._meta_client.factory.create('PackageTypeMembers')
            pkg_mem.name = name
            for m in members:
                pkg_mem.members.append(m)

        retrieve_request.unpackaged.types.append(pkg_mem)
        retrieve_response = self._meta_client.service.retrieve(retrieve_request)

        return retrieve_response

    def check_retrieve_status(self, id):
        self._setHeaders('checkRetrieveStatus')
        zip_response = self._meta_client.service.checkRetrieveStatus(id)
        zip_to_fs(zip_response)

        return True if zip_response else False 
