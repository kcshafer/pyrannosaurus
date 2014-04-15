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
