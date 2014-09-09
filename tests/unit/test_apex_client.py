import pytest

from pyrannosaurus.clients.base import BaseClient
from pyrannosaurus.clients.apex import ApexClient

from . import utils

base_client_mock = utils.ClientMock('wsdl/partner.xml')
apex_client_mock = utils.ClientMock('wsdl/apex.wsdl')

@pytest.fixture
def _login_result(*args):
    lr = base_client_mock.create_object('LoginResult')
    lr.sessionId = '123'
    lr.metadataServerUrl = "http://na1.salesforce.com/services/Soap/m/29.0/00Dx0000001T0zk"
    lr.serverUrl = "http://na1.salesforce.com/services/Soap/u/29.0/00Dx0000001T0zk"
    return lr

@pytest.fixture
def _multiple_login_result(*args):
    username =( args[1])[0]
    lr = base_client_mock.create_object('LoginResult')
    if username == 'usernameA':
        lr.sessionId = '123'
    else:
        lr.sessionId = '321'
    lr.metadataServerUrl = "http://na1.salesforce.com/services/Soap/m/29.0/00Dx0000001T0zk"
    lr.serverUrl = "http://na1.salesforce.com/services/Soap/u/29.0/00Dx0000001T0zk"
    return lr

def test_multiple_connections(monkeypatch):
    c = ApexClient()
    monkeypatch.setattr('suds.client.SoapClient.invoke', _multiple_login_result)
    c.login('usernameA', 'password', name='conn_a')
    c.login('usernameB', 'password', name='conn_b')

    print c._connections
    assert c._location == None

    c.set_active_connection('conn_a')

    assert c._sessionHeader['sessionId'] == '123'
    assert c._location == "http://na1.salesforce.com/services/Soap/u/29.0/00Dx0000001T0zk"

    c.set_active_connection('conn_b')
    assert c._sessionHeader['sessionId'] == '321'