"""Tests del webservice HotelService."""
import pytest
from suds.client import Client as SoapClient

_nombreServicio = 'HotelService'
_nombreModulo = 'imoreno'

@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    service_url = f"{base_url}/ws/{_nombreModulo}/{_nombreServicio}"
    wsdl_url = f"{service_url}?wsdl"
    return SoapClient(wsdl_url)


def test_wsdl_metadata(ws):
    """Test that our server provides valid WSDL metadata."""
    # First check the target namespace is correct. This will fail when you change the tns in the webservice.py
    assert ws.wsdl.tns == ("tns", f"com.{_nombreModulo}.{_nombreServicio}")

    # Inspect the service definition
    sd = ws.sd[0]
    assert sd.service.name == _nombreServicio
    # We have one port, named HotelService, that points to the root of the service ...
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == "HotelService"

    # Has 5 methods, and 12 types
    assert len(svc_port.methods) == 5
    assert len(sd.types) == 12


def test_service_methods(ws):
    """Test that our server provides the expected service methods."""
    # Inicialmente tenemos 2 clientes
    c = ws.service.listaClientes()
    assert len(c.Cliente) == 2
    assert c.Cliente[0].nombre == 'Juan'
    assert c.Cliente[1].nombre == 'Pedro'

    # Buscamos un cliente que existe
    op = ws.service.buscar("Juan", "Perez", "Gomez")
    assert op.nombre == "Juan"
    assert op.ap_primero == "Perez"
    assert op.ap_segundo == "Gomez"
    assert op.num_habitación == 101

    # # Agregamos un cliente
    op = ws.service.RegistroCliente("Maria", "Moreno", "Lopez", 103)
    assert op.status == "OK"

    # # Verificamos que si se agrego
    m = ws.service.BuscarCliente("Maria", "Moreno", "Lopez")
    assert m.nombre == "Maria"
    assert m.ap_primero == "Moreno"
    assert m.ap_segundo == "Lopez"
    assert m.num_habitación == 103
    
    # # Eliminamos el cliente ya agregado
    op = ws.service.BorrarCliente("Maria", "Moreno", "Lopez")
    assert op.status == "OK"

    # # Verificamos que si se elimino
    m = ws.service.BuscarCliente("Maria", "Moreno", "Lopez")
    assert m.status == "ERROR"

    # Actualizamos un cliente existente
    op = ws.service.ModificarCliente("Juan", "Perez", "Gomez", 105)
    assert op.status == "OK"

    # Verificamos que si se actualizo
    m = ws.service.BuscarCliente("Juan", "Perez", "Gomez")
    assert m.nombre == "Juan"
    assert m.ap_primero == "Perez"
    assert m.ap_segundo == "Gomez"
    assert m.num_habitación == 105
