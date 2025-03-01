"""Pruebas de mi servicio web, etapa 1.

En esta etapa solamente esta el esqueleto del servicio web. Las operaciones no realizan ninguna lógica de negocio.
"""
import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    service_url = f'{base_url}/ws/rgarcia/recetas'
    wsdl_url = f'{service_url}?wsdl'
    return SoapClient(wsdl_url)

def test_wsdl_metadata(ws):
    """Test that our server provides valid WSDL metadata."""
    # First check the target namespace is correct. This will fail when you change the tns in the webservice.py
    assert ws.wsdl.tns == ('tns', 'com.rgarcia.recetas')

    # Inspect the service definition
    sd = ws.sd[0]
    assert sd.service.name == 'RecetaService'
    # We have one port, named Recetas, that points to the root of the service ...
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == 'Recetas'

    # Has 6 methods, and 16 types
    assert len(svc_port.methods) == 6
    assert len(sd.types) == 16

def test_service_methods(ws):
    """Test that our server provides the expected service methods."""
    # Prueba para ver receta no existente
    op = ws.service.ver_receta()
    assert op.status == 'ERROR'
    assert op.message == 'No se encontro una receta con el nombre dado.'

    # prueba para ver receta existente
    op = ws.service.ver_receta('Tacos al Pastor')
    assert op.status == 'OK'
    assert op.message == 'Se encontro la receta con el nombre Tacos al Pastor.'

    #Prueba que exista 3 recetas en el catalogo inicial con ingredientes que inicien con Sal
    op = ws.service.buscar_por_ingrediente('Sal')
    assert op.status == 'OK'
    assert op.message == 'Se encontraron 3 recetas con el ingrediente Sal.'

    #Prueba que exista 1 receta en el catalogo inicial con ingredientes que inicien con Sal
    op = ws.service.buscar_por_ingrediente('Chile guajillo')
    assert op.status == 'OK'
    assert op.message == 'Se encontro una receta con el ingrediente Chile guajillo.'

    #Prueba que no existan recetas en el catalogo inicial con ingrediente Elote
    op = ws.service.buscar_por_ingrediente('Torta')
    assert op.status == 'OK'
    assert op.message == 'No se encontraron recetas con el ingrediente dado.'

    #Prueba para comprobar al duplicar receta
    op = ws.service.registrar("Tacos al Pastor", "descripcion", [], [])
    assert op.status == 'ERROR'
    assert op.message == 'Ya existe una receta con el nombre dado.'

    #Prueba para comprar insercion de receta
    op = ws.service.registrar("Taco de Pizza", "descripcion", [], [])
    assert op.status == 'OK'
    assert op.message == 'Se agrego receta nueva.'


    #Prueba para actualizar receta existente
    op = ws.service.actualizar("Tacos al Pastor", "descripcion", [], [])
    assert op.status == 'OK'
    assert op.message == 'Se actualizo la receta correctamente.'

    #Prueba para actualizar receta no existente
    op = ws.service.actualizar("Taco de Hamburguesa", "descripcion", [], [])
    assert op.status == 'ERROR'
    assert op.message == 'No se encontro la receta con el nombre dado.'

    #Prueba para borrar receta existente
    op = ws.service.borrar("Tacos al Pastor")
    assert op.status == 'OK'
    assert op.message == 'Se borro la receta con nombre Tacos al Pastor.'

    #Prueba para borrar receta no existente
    op = ws.service.borrar("Tacos Gobernador")
    assert op.status == 'ERROR'
    assert op.message == 'No se encontro una receta con el nombre dado.'
