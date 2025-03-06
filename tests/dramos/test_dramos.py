import pytest
from suds.client import Client as SoapClient

@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    wsdl_url = f'{base_url}/ws/dramos?wsdl'
    return SoapClient(wsdl_url)

def test_wsdl_metadata(ws):
    """Test que verifica la validez del WSDL del servidor SOAP."""
    #  Verifica que el target namespace sea correcto
    assert ws.wsdl.tns == ('tns', 'com.dramos.productos')

    #  Inspecciona la definición del servicio
    sd = ws.sd[0]
    assert sd.service.name == 'ProductosService'

    #  Debe haber un solo puerto
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == 'Productos'

    #  Debe haber 4 métodos y 10 tipos de datos
    assert len(svc_port.methods) == 4
    assert len(sd.types) == 10

def test_service_methods(ws):
    """Test que verifica el correcto funcionamiento del servicio SOAP."""
    
    #  Verificamos la lista inicial de productos
    productos = ws.service.listado()
    assert len(productos.Producto) == 2
    assert productos.Producto[0].nombre == 'Coca-cola'
    assert productos.Producto[0].categoria == 'Refresco'

    #  Registramos un nuevo producto
    dato = ws.service.registrar('Pepsi', 'Refresco')
    assert dato == "Producto registrado"

    #  Verificamos que el producto se haya agregado correctamente
    productos = ws.service.listado()
    assert len(productos.Producto) == 3
    assert productos.Producto[0].nombre == 'Coca-cola'
    assert productos.Producto[0].categoria == 'Refresco'

    #  Eliminamos el producto "Pepsi"
    dato = ws.service.eliminar('Pepsi')
    assert dato == "Producto eliminado correctamente"

    #  Verificamos que "Pepsi" haya sido eliminado
    productos = ws.service.listado()
    assert len(productos.Producto) == 2
    assert productos.Producto[0].nombre == 'Coca-cola'
    assert productos.Producto[0].categoria == 'Refresco'

    #  Editamos la categoría de "Coca-cola"
    dato = ws.service.editar('Coca-cola', 'Jugo')
    assert dato == "Producto actualizado correctamente"

    #  Verificamos que "Coca-cola" haya cambiado de categoría
    productos = ws.service.listado()
    assert len(productos.Producto) == 2
    assert productos.Producto[0].nombre == 'Coca-cola'
    assert productos.Producto[0].categoria == 'Jugo'
