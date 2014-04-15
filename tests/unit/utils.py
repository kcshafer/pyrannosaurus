import os

from suds.client import Client

class ClientMock(object):

    def __init__(self, wsdl):
        cache = None
        wsdl = 'wsdl/partner.xml'
        if '://' not in wsdl:
            if os.path.isfile(wsdl):
                wsdl = 'file://' + os.path.abspath(wsdl)
        self._client = Client(wsdl, cache=cache)

    def create_object(self, name):
        try:
            return self._client.factory.create(name)
        except:
            #TODO: should be real exception
            return "Object not found"
