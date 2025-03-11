
"""Test del webservice de gestión de cursos."""

import pytest
from suds.client import Client as SoapClient # type: ignore

@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    service_url = f"{base_url}/ws/jchaidez/gestion_cursos"
    wsdl_url = f"{service_url}?wsdl"
    return SoapClient(wsdl_url)

def test_wsdl_metadata(ws):
    """Test que verifica que el servidor proporciona metadatos WSDL válidos."""
    assert ws.wsdl.tns == ("tns", "gestorcursos")
    
    sd = ws.sd[0]
    assert sd.service.name == "CursoService"
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == "CursoService"
    
    assert len(svc_port.methods) == 5
    assert len(sd.types) == 14
    
def test_buscar_curso_error(ws):
    """Test que verifica que la búsqueda de un curso sin nombre o ID devuelve un error."""
    response = ws.service.buscar_curso(None, None)  # Pasamos ambos como None
    assert response['status'] == 'ERROR'
    assert response['mensaje'] == 'Debe especificar nombre o ID'
    
def test_agregar_curso_con_id_existente(ws):
    """Test que verifica que no se puede agregar un curso con un ID ya existente."""
    # Intentamos agregar un curso con un ID que ya existe
    response = ws.service.agregar_curso(1, "Nuevo Curso", "Nuevo Profesor")
    
    # Verificamos que la respuesta sea la esperada
    assert response['status'] == 'ERROR'
    assert response['mensaje'] == 'El ID del curso ya existe'
    
def test_buscar_curso_no_encontrado(ws):
    """Test que verifica que la búsqueda de un curso inexistente devuelve un error."""
    # Intentamos buscar un curso que no existe
    response = ws.service.buscar_curso("Curso Inexistente", None)  # Usamos un nombre que no existe
    
    # Verificamos que la respuesta sea la esperada
    assert response['status'] == 'ERROR'
    assert response['mensaje'] == 'Curso no encontrado'

def test_service_methods(ws):
    """Test que verifica las operaciones CRUD del servicio de cursos."""
    # Inicialmente tenemos 4 cursos
    m = ws.service.listado_cursos()
    assert len(m.Curso) == 4
    assert m.Curso[0].nombre == "Programación en Python"
    assert m.Curso[1].nombre == "Bases de Datos SQL"
    assert m.Curso[2].nombre == "Inteligencia Artificial"
    assert m.Curso[3].nombre == "Taller de Sistemas Operativos"

    # Buscar un curso existente por nombre
    op = ws.service.buscar_curso("Programación en Python")
    assert op['status'] == 'OK'  # Usamos 'status' ya que la respuesta es un diccionario
    assert op['nombre'] == "Programación en Python"  # Accedemos a 'nombre' correctamente
    assert op['profesor'] == "Noe Nieto"

    # Agregar un nuevo curso
    op = ws.service.agregar_curso(6, "Ecuaciones Diferenciales", "Lupita Amado")
    assert op['status'] == "OK"
    assert op['nombre'] == "Ecuaciones Diferenciales"
    assert op['profesor'] == "Lupita Amado"

    # Verificar que se agregó correctamente
    m = ws.service.listado_cursos()
    assert len(m.Curso) == 5

    # Eliminar un curso
    op = ws.service.eliminar_curso(id_curso=6)
    assert op['status'] == "OK"

    # Verificar eliminación
    m = ws.service.listado_cursos()
    assert len(m.Curso) == 4

    # Intentar buscar un curso eliminado
    op = ws.service.buscar_curso("Ecuaciones Diferenciales")
    assert op['status'] == "ERROR"

    # Actualizar un curso existente
    op = ws.service.actualizar_curso(1, "Bases de Datos NoSQL", "Carolina Ruiz")
    assert op['status'] == "OK"

    # Verificar actualización
    op = ws.service.buscar_curso("Bases de Datos NoSQL")
    assert op['nombre'] == "Bases de Datos NoSQL"  # Accedemos a 'nombre' correctamente

    # Pruebas de error
    op = ws.service.actualizar_curso(999, "Nuevo Curso", "Profesor")
    assert op['status'] == "ERROR"

    op = ws.service.eliminar_curso(999)
    assert op['status'] == "ERROR"

    op = ws.service.agregar_curso(1, "Curso duplicado", "Profesor")
    assert op['status'] == "ERROR"