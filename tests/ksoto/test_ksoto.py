import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    service_url = f'{base_url}/ws/ksoto/peliculas'
    wsdl_url = f'{service_url}?wsdl'
    return SoapClient(wsdl_url)





def test_wsdl_metadata(ws):
    """Test that our server provides valid WSDL metadata."""
    # First check the target namespace is correct. This will fail when you change the tns in the webservice.py
    assert ws.wsdl.tns == ('tns', 'com.ksoto.movies')

    # Inspect the service definition
    sd = ws.sd[0]
    assert sd.service.name == 'MoviesServices'
    # We have one port, named Alcancia, that points to the root of the service ...
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == 'Movies'

    # Has 4 methods and 3 types
    assert len(svc_port.methods) == 5
    assert len(sd.types) == 12



def test_service_methods(ws):
    
    assert len(ws.service.getMovies()) == 0





# corremos --->    uv run pytest
# Tenemos que ejecutar el comando en ksoto