from fastapi.testclient import TestClient 
from main import app,API_TOKEN 

client=TestClient(app)


def test_unauthorized_access():
    response=client.post('/extract',data={'prompt':'test'})
    assert response.status_code==422



def test_auth_failure():
    response=client.post('/extract',
                         headers={'x-api-token':'wrong'},
                         data={'prompt':'test'})
    assert response.status_code==401