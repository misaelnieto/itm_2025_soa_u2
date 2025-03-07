"""Tests del webservice HotelService."""
from suds.client import Client as SoapClient

_nombreServicio = 'HotelService'
_nombreModulo = 'imoreno'

def test_wsdl_metadata(wsgi_live_server):
    """Test that our server provides a valid WSDL metadata."""
    base_url = wsgi_live_server
    service_url = f'{base_url}/ws/{_nombreModulo}/{_nombreServicio}/v1'
    wsdl_url = f'{service_url}?wsdl'
    ws = SoapClient(wsdl_url)

    # First check the target namespace is correct. This will fail when you change the tns in the webservice.py
    assert ws.wsdl.tns == ('tns', f'com.{_nombreModulo}.{_nombreServicio}')

    # Inspect the service definition
    sd = ws.sd[0]
    assert sd.service.name == _nombreServicio

    # We have one port, named HotelService, that points to the root of the service ...
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == 'HotelService'
    assert svc_port.location == service_url

    # Has 4 methods, and 11 types
    assert len(svc_port.methods) == 2
    assert len(sd.types) == 12


def test_service_methods(wsgi_live_server):
    """Test that our server provides the expected service methods."""
    base_url = wsgi_live_server
    service_url = f'{base_url}/ws/{_nombreModulo}/{_nombreServicio}/v1'
    wsdl_url = f'{service_url}?wsdl'
    ws = SoapClient(wsdl_url)

    # Check the service methods
    assert ws.service.registroCliente('Isaí', 'Moreno', 'Mendoza', 100) == {'status': 'OK', 'message': [{'nombre': 'Isaí', 'ap_primero': 'Moreno', 'ap_segundo': 'Mendoza', 'num_habitacion': 100}]}
    assert ws.service.BuscarCliente('Isaí', 'Moreno', 'Mendoza') == {'nombre': 'Isaí', 'ap_primero': 'Moreno', 'ap_segundo': 'Mendoza', 'num_habitacion': 100}
    c = ws.service.Cliente()
    assert len(c.Cliente) == 4


