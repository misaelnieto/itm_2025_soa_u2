"""Módulo de pruebas para el servicio SOAP de productos.

Verifica el correcto funcionamiento de las operaciones CRUD.
"""

import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    wsdl_url = f"{base_url}/ws/dramos?wsdl"
    return SoapClient(wsdl_url)


def test_wsdl_metadata(ws):
    """Verifica la validez del WSDL del servidor SOAP."""
    assert ws.wsdl.tns == ("tns", "com.dramos.productos")

    # Inspecciona la definición del servicio
    sd = ws.sd[0]
    assert sd.service.name == "ProductosService"

    # Debe haber un solo puerto
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == "Productos"

    # Debe haber 4 métodos
    assert len(svc_port.methods) == 4


def test_service_methods(ws):
    """Verifica el correcto funcionamiento del servicio SOAP."""
    # Verificamos la lista inicial de productos
    productos = ws.service.listado()
    assert len(productos.Producto) == 2
    assert productos.Producto[0].nombre == "Coca-cola"
    assert productos.Producto[0].categoria == "Refresco"
    assert productos.Producto[0].precio == "15"

    # Registramos un nuevo producto con precio
    dato = ws.service.registrar("Pepsi", "Refresco", "18")
    assert dato == "Producto registrado"

    # Verificamos que el producto se haya agregado correctamente
    productos = ws.service.listado()
    assert len(productos.Producto) == 3
    assert productos.Producto[2].nombre == "Pepsi"
    assert productos.Producto[2].categoria == "Refresco"
    assert productos.Producto[2].precio == "18"

    # Eliminamos el producto "Pepsi"
    dato = ws.service.eliminar("Pepsi")
    assert dato == "Producto eliminado correctamente"

    # Verificamos que "Pepsi" haya sido eliminado
    productos = ws.service.listado()
    assert len(productos.Producto) == 2
    assert productos.Producto[0].nombre == "Coca-cola"
    assert productos.Producto[0].categoria == "Refresco"

    # Editamos la categoría y el precio de "Coca-cola"
    dato = ws.service.actualizar("Coca-cola", "Jugo", "20")
    assert dato == "Producto actualizado correctamente"

    # Verificamos que "Coca-cola" haya cambiado de categoría y precio
    productos = ws.service.listado()
    assert len(productos.Producto) == 2
    assert productos.Producto[0].nombre == "Coca-cola"
    assert productos.Producto[0].categoria == "Jugo"
    assert productos.Producto[0].precio == "20"

    # Intentamos eliminar un producto que no existe
    dato = ws.service.eliminar("Pepsi")
    assert dato == "Producto no encontrado"

    # Intentamos actualizar un producto que no existe
    dato = ws.service.actualizar("Fanta", "Soda", "25")
    assert dato == "Producto no encontrado"
