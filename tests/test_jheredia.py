"""Este módulo contiene las pruebas para los servicios relacionados con las ciudades.

incluyendo operaciones como listado, registro, eliminación y actualización de ciudades.
"""

import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    wsdl_url = f"{base_url}/ws/jheredia?wsdl"
    return SoapClient(wsdl_url)


def test_wsdl_metadata(ws):
    """Verifica la validez del WSDL del servidor SOAP."""
    assert ws.wsdl.tns == ("tns", "com.jheredia.ciudades")

    # Inspecciona la definición del servicio
    sd = ws.sd[0]
    assert sd.service.name == "CiudadesService"

    # Debe haber un solo puerto
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == "Ciudades"

    # Debe haber 4 métodos
    assert len(svc_port.methods) == 4  # Ahora debe ser 4 debido a que actualizamos el servicio


def test_service_methods(ws):
    """Verifica el correcto funcionamiento del servicio SOAP."""
    # Verificamos la lista inicial de ciudades
    ciudades = ws.service.listado()
    assert len(ciudades.Ciudad) == 2
    assert ciudades.Ciudad[0].nombre == "Mexicali"
    assert ciudades.Ciudad[0].pais == "México"
    assert ciudades.Ciudad[0].poblacion == "1,000,000"

    # Re
