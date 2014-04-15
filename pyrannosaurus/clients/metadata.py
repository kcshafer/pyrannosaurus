import string
import sys
import os.path

from suds.client import Client
from suds.cache import FileCache

from pyrannosaurus.clients.base import BaseClient
from pyrannosaurus.utils import package_to_dict

class MetadataClient(BaseClient):

    def __init__(self, wsdl='wsdl/metadata.xml', cacheDuration = 0, **kwargs):
        super(MetadataClient, self).__init__()
        #TODO: clean this up
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

    #TODO eval
    def _setHeaders(self, call = None):
        headers = {'SessionHeader': self._sessionHeader}

        if call == 'login':
            if self._loginScopeHeader is not None:
                headers['LoginScopeHeader'] = self._loginScopeHeader
            self._base_client.set_options(soapheaders = headers)

        self._meta_client.set_options(soapheaders = headers)


    def login(self, username, password, token=''):
        super(MetadataClient, self)._login(username, password, token)

    def deploy(self, file_path, **kwargs):
        self._setHeaders('retrieve')
        deploy_options = self._meta_client.factory.create('DeployOptions')
        deploy_options.allowMissingFiles = False
        deploy_options.autoUpdatePackage = False
        deploy_options.checkOnly = False
        deploy_options.ignoreWarnings = False
        deploy_options.performRetrieve = False
        deploy_options.purgeOnDelete = False
        deploy_options.rollbackOnError = True
        deploy_options.runAllTests = False
        deploy_options.runTests = []
        deploy_options.singlePackage = True
        if kwargs:
            for k, v in kwargs.iteritems():
                    if k in deploy_options.__keylist__:
                        deploy_options.__setattr__(k,v)

        res = self._meta_client.service.deploy(zip_to_binary(file_path), deploy_options)
        return res

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
        return zip_response

    def cancel_deploy(self, id):
        self._setHeaders('cancelDeploy')
        if id:
            cancel_deploy_result = self._meta_client.service.cancelDeploy(id)
            return cancel_deploy_result
        else:
            #TODO: probably should impl this as exception
            return 'Must specify id for cancel deploy call.'

    def check_status(self, id):
        self._setHeaders('checkStatus')
        if id:
            async_result = self._meta_client.service.checkStatus(id)
            return async_result
        else:
            #TODO: probably should impl this as exception
            return 'Must specify id for check status call.'
