"""Este m\u00f3dulo contiene las pruebas para los servicios relacionados con las ciudades.

Incluye operaciones como listado, registro, eliminaci\u00f3n y actualizaci\u00f3n de ciudades.
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

    # Inspecciona la definici\u00f3n del servicio
    sd = ws.sd[0]
    assert sd.service.name == "CiudadesService"

    # Debe haber un solo puerto
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == "Ciudades"

    # Debe haber 4 m\u00e9todos
    assert len(svc_port.methods) == 4


def test_service_methods(ws):
    """Verifica el correcto funcionamiento del servicio SOAP."""
    # Verificamos la lista inicial de ciudades
    ciudades = ws.service.listado()
    assert len(ciudades.Ciudad) == 2
    assert ciudades.Ciudad[0].nombre == "Mexicali"
    assert ciudades.Ciudad[0].pais == "M\u00e9xico"
    assert ciudades.Ciudad[0].poblacion == "1,000,000"

    # Prueba de registro de una nueva ciudad
    response = ws.service.registrar("Ensenada", "M\u00e9xico", "500,000")
    assert response == "Ciudad registrada"

    # Verificar que la ciudad fue agregada
    ciudades = ws.service.listado()
    assert any(c.nombre == "Ensenada" for c in ciudades.Ciudad)

    # Verificar el uso de la línea 46 (ciudades_filtradas)
    response = ws.service.eliminar("CiudadInexistente")
    assert response == "Ciudad no encontrada"

    # Prueba de actualizaci\u00f3n de una ciudad
    response = ws.service.actualizar("Ensenada", "M\u00e9xico", "600,000")
    assert response == "Ciudad actualizada correctamente"

    # Verificar que la ciudad fue actualizada
    ciudades = ws.service.listado()
    ensenada = next(c for c in ciudades.Ciudad if c.nombre == "Ensenada")
    assert ensenada.poblacion == "600,000"

    # Prueba de eliminaci\u00f3n de una ciudad
    response = ws.service.eliminar("Ensenada")
    assert response == "Ciudad eliminada correctamente"

    # Verificar que la ciudad fue eliminada
    ciudades = ws.service.listado()
    assert not any(c.nombre == "Ensenada" for c in ciudades.Ciudad)

    # Verificar el uso de la línea 59 (actualización fallida)
    response = ws.service.actualizar("CiudadInexistente", "OtroPaís", "700,000")
    assert response == "Ciudad no encontrada"
