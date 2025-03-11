"""Este módulo contiene las pruebas para los servicios relacionados con los carros.

Incluye operaciones como listado, registro, eliminación y actualización de carros.
"""

import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    wsdl_url = f"{base_url}/ws/fcalzada?wsdl"
    return SoapClient(wsdl_url)


def test_wsdl_metadata(ws):
    """Verifica la validez del WSDL del servidor SOAP."""
    assert ws.wsdl.tns == ("tns", "com.fcalzada.carros")

    # Inspecciona la definición del servicio
    sd = ws.sd[0]
    assert sd.service.name == "CarrosService"

    # Debe haber un solo puerto
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == "Carros"

    # Debe haber 4 métodos
    assert len(svc_port.methods) == 4


def test_service_methods(ws):
    """Verifica el correcto funcionamiento del servicio SOAP."""
    # Verificamos la lista inicial de carros
    carros = ws.service.listado()
    assert len(carros.Carro) == 2
    assert carros.Carro[0].marca == "Toyota"
    assert carros.Carro[0].modelo == "Corolla"
    assert carros.Carro[0].año == "2020"

    # Prueba de registro de un nuevo carro
    response = ws.service.registrar("Honda", "Civic", "2022")
    assert response == "Carro registrado"

    # Verificar que el carro fue agregado
    carros = ws.service.listado()
    assert any(c.marca == "Honda" and c.modelo == "Civic" for c in carros.Carro)

    # Prueba de eliminación de un carro
    response = ws.service.eliminar("Honda", "Civic")
    assert response == "Carro eliminado correctamente"

    # Verificar que el carro fue eliminado
    carros = ws.service.listado()
    assert not any(c.marca == "Honda" and c.modelo == "Civic" for c in carros.Carro)

    # Prueba de actualización de un carro
    response = ws.service.actualizar("Toyota", "Corolla", "2021")
    assert response == "Carro actualizado correctamente"

    # Verificar que el carro fue actualizado
    carros = ws.service.listado()
    corolla = next(c for c in carros.Carro if c.marca == "Toyota" and c.modelo == "Corolla")
    assert corolla.año == "2021"

    # Prueba de eliminación de un carro inexistente
    response = ws.service.eliminar("Ford", "Mustang")
    assert response == "Carro no encontrado"

    # Prueba de actualización de un carro inexistente
    response = ws.service.actualizar("Ford", "Mustang", "2023")
    assert response == "Carro no encontrado"
