"""Este módulo contiene las pruebas para los servicios relacionados con las ventas.

Incluye operaciones como listado, registro, eliminación y actualización de ventas.
"""

import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Inicializa un cliente SOAP para el servidor WSGI.""" 
    base_url = wsgi_live_server
    wsdl_url = f"{base_url}/ws/jcontreras?wsdl"
    return SoapClient(wsdl_url)


def test_wsdl_metadata(ws):
    """Verifica la validez del WSDL del servidor SOAP.""" 
    assert ws.wsdl.tns == ("tns", "com.jcontreras.ventas")

    # Inspecciona la definición del servicio
    sd = ws.sd[0]
    assert sd.service.name == "VentasService"

    # Debe haber un solo puerto
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == "Ventas"

    # Debe haber 4 métodos
    assert len(svc_port.methods) == 4


def test_service_methods(ws):
    """Verifica el correcto funcionamiento del servicio SOAP.""" 
    # Verificamos la lista inicial de ventas
    ventas = ws.service.listado()
    assert len(ventas.Venta) == 2
    assert ventas.Venta[0].producto == "Laptop"
    assert ventas.Venta[0].cantidad == 1
    assert ventas.Venta[0].precio == 1500.00
    assert ventas.Venta[0].total == 1500.00

    # Prueba de registro de una nueva venta
    response = ws.service.registrar("Tablet", 3, 350.00)
    assert response == "Venta registrada"

    # Verificar que la venta fue agregada
    ventas = ws.service.listado()
    assert any(v.producto == "Tablet" for v in ventas.Venta)

    # Verificar el uso de la línea 46 (ventas_filtradas)
    response = ws.service.eliminar("ProductoInexistente")
    assert response == "Venta no encontrada"

    # Prueba de actualización de una venta
    response = ws.service.actualizar("Tablet", 300.00, 4)
    assert response == "Venta actualizada correctamente"

    # Verificar que la venta fue actualizada
    ventas = ws.service.listado()
    tablet = next(v for v in ventas.Venta if v.producto == "Tablet")
    assert tablet.precio == 300.00
    assert tablet.cantidad == 4
    assert tablet.total == 1200.00

    # Prueba de eliminación de una venta
    response = ws.service.eliminar("Tablet")
    assert response == "Venta eliminada correctamente"

    # Verificar que la venta fue eliminada
    ventas = ws.service.listado()
    assert not any(v.producto == "Tablet" for v in ventas.Venta)

    # Verificar el uso de la línea 59 (actualización fallida)
    response = ws.service.actualizar("ProductoInexistente", 400.00, 5)
    assert response == "Venta no encontrada"
