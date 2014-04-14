import string
import sys
import os.path

from suds.client import Client
from suds.cache import FileCache

class LoginClient(object):
    '''
        LoginClient uses suds to wrap the SF partner wsdl, but really only uses
        the login method
    '''

    _sessionHeader = None
    _product = 'Metadata Tool'
    _version = (0, 0, 0)
    _location = None

    _loginScopeHeader = None

    def __init__(self, wsdl='wsdl/partner.xml', cacheDuration = 0, **kwargs):
        if cacheDuration > 0:
            cache = FileCache()
            cache.setduration(seconds = cacheDuration)
        else:
            cache = None

        headers = {'User-Agent': 'Salesforce/' + self._product + '/' + '.'.join(str(x) for x in self._version)}
        self._login_client.set_options(headers = headers)
