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
    # Inicialmente tenemos 2 libros
    c = ws.service.listaClientes()
    assert len(c.Cliente) == 2
    assert c.Cliente[0].nombre == 'Juan'
    assert c.Cliente[1].nombre == 'Pedro'

    # Buscamos un libro que existe
    """op = ws.service.buscar("El señor de los anillos")
    assert op.titulo == "El señor de los anillos"
    assert op.autor == "J.R.R. Tolkien"""

    # # Agregamos un libro
    """ op = ws.service.agregar("El Silmarillion", "J.R.R. Tolkien", 41234)
    assert op.titulo == "El Silmarillion"
    assert op.autor == "J.R.R. Tolkien"
    assert op.status == "OK" """

    # # Verificamos que si se agrego
    """m = ws.service.listado()
    assert len(m.Libro) == 3
    assert m.Libro[0].titulo == "El señor de los anillos"
    assert m.Libro[1].titulo == "El hobbit"
    assert m.Libro[2].titulo == "El Silmarillion"""
    
    """# # Eliminamos el libro ya agregado
    op = ws.service.eliminar(isbn=41234)
    assert op.status == "OK"""

    # # Verificamos que si se elimino
    """m = ws.service.listado()
    assert len(m.Libro) == 2
    assert m.Libro[0].titulo == "El señor de los anillos"
    assert m.Libro[1].titulo == "El hobbit"""

    # # Intentamos buscar un libro ya eliminado y la respuesta del server es de ERROR
    """op = ws.service.buscar("El Silmarillion")
    assert op.status == "ERROR"""

    # Actualizamos un libro existente
    """ op = ws.service.actualizar(12345, "El señor de los anillos 2", "J.R.R. Tolkien")
    assert op.status == "OK" """

    # Verificamos que si se actualizo
    """ op = ws.service.buscar("El señor de los anillos 2")
    assert op.titulo == "El señor de los anillos 2"

    op = ws.service.actualizar(1231241)
    assert op.status == "ERROR"

    op = ws.service.eliminar(123124112)
    assert op.status == "ERROR"

    op = ws.service.agregar("El Silmarillion", "J.R.R. Tolkien", 12345)
    assert op.status == "ERROR" """
