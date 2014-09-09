import pytest

from pyrannosaurus.clients.base import BaseClient
from . import utils

base_client_mock = utils.ClientMock('wsdl/partner.xml')

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

def test_login(monkeypatch):
    c = BaseClient()
    monkeypatch.setattr('suds.client.SoapClient.invoke', _login_result)
    response, header = c._login('username', 'password')
    assert response, 'Login response was not created'
    assert response.sessionId == '123', 'Login response sessionId is incorrect'

def test_multiple_connections(monkeypatch):
    c = BaseClient()
    monkeypatch.setattr('suds.client.SoapClient.invoke', _multiple_login_result)
    c.login('usernameA', 'password', name='conn_a')
    c.login('usernameB', 'password', name='conn_b')

    assert c._sessionHeader == None
    assert c._location == None

    c.set_active_connection('conn_a')

    assert c._sessionHeader['sessionId'] == '123'
    assert c._location == "http://na1.salesforce.com/services/Soap/u/29.0/00Dx0000001T0zk"

    c.set_active_connection('conn_b')
    assert c._sessionHeader['sessionId'] == '321'

def test_create_generic_sobject_without_type():
    c = BaseClient()
    so = c.create_generic_sobject()

    assert so, 'Generic sobject was not created'
    assert so.type == None, 'Generic sobject was not returned with a None type'

def test_create_generic_sobject_without_type():
    c = BaseClient()
    so = c.create_generic_sobject(type='Account')

    assert so, 'Generic sobject was not created'
    assert so.type == 'Account', 'Generic sobject was returned without a type'

def test_create_generic_sobject_with_kwargs():
    c = BaseClient()
    so = c.create_generic_sobject(Name='test name', BillingStreet='123 Test St.')

    assert so, 'Generic SObject was not created'
    assert so.Name == 'test name', 'Generic sobject name should be test name but is %s ' % so.Name
    assert so.BillingStreet == '123 Test St.', 'Generic sobject BillingStreet should be 123 Test St. but is %s ' % so.BillingStreet

def test_create_generic_sobject_with_kwargs_and_type():
    c = BaseClient()
    so = c.create_generic_sobject(type='Account', Name='test name', BillingStreet='123 Test St.')

    assert so, 'Generic SObject was not created'
    assert so.type == 'Account', 'Generic sobject was returned without a type'
    assert so.Name == 'test name', 'Generic sobject name should be test name but is %s ' % so.Name
    assert so.BillingStreet == '123 Test St.', 'Generic sobject BillingStreet should be 123 Test St. but is %s ' % so.BillingStreet