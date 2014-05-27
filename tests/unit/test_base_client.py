import pytest

from pyrannosaurus.clients.base import BaseClient
from . import utils

base_client_mock = utils.ClientMock('wsdl/partner.xml')

@pytest.fixture
def _login_result(*args):
    lr = base_client_mock.create_object('LoginResult')
    lr.sessionId = '123'
    return lr

def test_login(monkeypatch):
    c = BaseClient()
    monkeypatch.setattr('suds.client.SoapClient.invoke', _login_result)
    response = c._login('username', 'password')
    assert response, 'Login response was not created'
    assert response.sessionId == '123', 'Login response sessionId is incorrect'

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