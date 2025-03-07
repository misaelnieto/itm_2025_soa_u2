"""Test para servicio web eventos."""
import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    wsdl_url = f'{base_url}/ws/imayo/eventos?wsdl'  # Actualiza la URL WSDL
    return SoapClient(wsdl_url)


def test_wsdl_metadata(ws):
    """Test que verifica que el servidor proporciona metadatos WSDL válidos."""
    # Comprobamos que el namespace sea el correcto
    assert ws.wsdl.tns == ('tns', 'com.imayo.eventos')
    # Inspeccionamos la definición del servicio
    sd = ws.sd[0]
    assert sd.service.name == 'EventosService'
    # Verificamos que haya un solo puerto
    assert len(sd.service.ports) == 1  # Debería haber un solo puerto
    svc_port = sd.service.ports[0]
    assert svc_port.name == 'Eventos'
    # Verificamos que existan los métodos esperados
    assert len(svc_port.methods) == 5  # Métodos: crear, leer, actualizar, eliminar, listar
    
def test_listado(ws):
    """Este metodo hace un test del listado que tiene los eventos."""
    eventos = ws.service.listado()
    assert len(eventos.Evento) == 3
    assert eventos.Evento[0].nombre=="Boda"
    assert eventos.Evento[0].descripcion=="Se casan"


def test_crear_evento(ws):
    """Test que verifica la creación de un evento."""
    respuesta = ws.service.crear_evento("Evento Test", "Descripción del Evento")
    assert respuesta == "Evento creado exitosamente"


def test_crear_evento_existente(ws):
    """Test que verifica la creación de un evento existente."""
    ws.service.crear_evento("Evento Duplicado", "Descripción del Evento 1")
    respuesta = ws.service.crear_evento("Evento Duplicado", "Nueva descripción")
    assert respuesta == "Evento ya existe"


def test_leer_evento(ws):
    """Test que verifica la lectura de un evento."""
    ws.service.crear_evento("Evento Leer", "Leer descripción")
    evento = ws.service.leer_evento("Evento Leer")
    assert evento["descripcion"] == "Leer descripción"


def test_leer_evento_no_existente(ws):
    """Test que verifica la lectura de un evento no existente."""
    evento = ws.service.leer_evento("Evento Inexistente")
    # Ajustamos para manejar `None` en lugar de `{}`.
    assert evento is None  # Esperamos que sea None en lugar de un diccionario vacío.


def test_actualizar_evento(ws):
    """Test que verifica la actualización de un evento."""
    ws.service.crear_evento("Evento Viejo", "Descripción vieja")
    respuesta = ws.service.actualizar_evento("Evento Viejo", "Descripción nueva")
    assert respuesta == "Evento actualizado exitosamente"
    evento = ws.service.leer_evento("Evento Viejo")
    assert evento["descripcion"] == "Descripción nueva"


def test_actualizar_evento_no_existente(ws):
    """Test que verifica la actualización de un evento no existente."""
    respuesta = ws.service.actualizar_evento("Evento Inexistente", "Nueva descripción")
    assert respuesta == "Evento no existe"


def test_eliminar_evento(ws):
    """Test que verifica la eliminación de un evento."""
    ws.service.crear_evento("Evento Test", "Descripción del Evento")
    respuesta = ws.service.eliminar_evento("Evento Test")
    assert respuesta == "Evento eliminado exitosamente"
    evento = ws.service.leer_evento("Evento Test")
    # Ajustamos para manejar `None` en lugar de `{}`.
    assert evento is None  # Esperamos que sea None después de la eliminación.


def test_eliminar_evento_no_existente(ws):
    """Test que verifica la eliminación de un evento no existente."""
    respuesta = ws.service.eliminar_evento("Evento Inexistente")
    assert respuesta == "Evento no existe"



    

    







