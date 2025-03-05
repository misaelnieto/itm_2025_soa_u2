import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    wsdl_url = f'{base_url}/ws/ffernadez?wsdl'
    return SoapClient(wsdl_url)


def test_wsdl_metadata(ws):
    """Test that our server provides valid WSDL metadata."""
    # First check the target namespace is correct. This will fail when you change the tns in the webservice.py
    assert ws.wsdl.tns == ('tns', 'com.ffernandez.perritos')

    # Inspect the service definition
    sd = ws.sd[0]
    assert sd.service.name == 'PerritosService'
    # We have one port, named Alcancia, that points to the root of the service ...
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == 'Perritos'

    # Has 4 methods, and 11 types
    assert len(svc_port.methods) == 4
    assert len(sd.types) == 10



def test_service_methods(ws):
    """Test that our server provides the expected service methods."""
    # Probamos la lista de perritos
    perritos = ws.service.listado()
    assert len(perritos.Perrito) == 4
    assert perritos.Perrito[0].nombre == 'Lucy'
    assert perritos.Perrito[0].raza == 'Cocker'

    respuesta = ws.service.registrar('Bombon', 'Chihuahua')
    assert respuesta == 'OK'

    respuesta = ws.service.editar('Bombon', 'Mixta')
    assert respuesta == 'OK'

    respuesta = ws.service.eliminar('Bombon')
    assert respuesta == 'OK'

