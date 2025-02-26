"""Pruebas de mi servicio web, etapa 1.

En esta etapa solamente esta el esqueleto del servicio web. Las operaciones no realizan ninguna lógica de negocio.
"""
from suds.client import Client as SoapClient


def test_wsdl_metadata(wsgi_live_server):
    """Test that our server provides a valid WSDL metadata."""
    base_url = wsgi_live_server
    service_url = f'{base_url}/ws/nnieto/alcancia/v1'
    wsdl_url = f'{service_url}?wsdl'
    ws = SoapClient(wsdl_url)

    # First check the target namespace is correct. This will fail when you change the tns in the webservice.py
    assert ws.wsdl.tns == ('tns', 'com.noenieto.alcancia')

    # Inspect the service definition
    sd = ws.sd[0]
    assert sd.service.name == 'AlcanciaService'

    # We have one port, named Alcancia, that points to the root of the service ...
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == 'Alcancia1'
    assert svc_port.location == service_url

    # Has 4 methods, and 11 types
    assert len(svc_port.methods) == 4
    assert len(sd.types) == 12


def test_service_methods(wsgi_live_server):
    """Test that our server provides the expected service methods."""
    base_url = wsgi_live_server
    service_url = f'{base_url}/ws/nnieto/alcancia/v1'
    wsdl_url = f'{service_url}?wsdl'
    ws = SoapClient(wsdl_url)

    # Check the service methods
    assert ws.service.saldo() == 100
    assert ws.service.deposito(100) == 100 * 2
    assert ws.service.retiro(100) == 100 * 3
    m = ws.service.movimientos()
    assert len(m.Movimiento) == 3


