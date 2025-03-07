"""Este es el modulo para realizar las pruebas de nuestro servicio.

"""""

import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    service_url = f'{base_url}/ws/dduenas/estudiantes'
    wsdl_url = f'{service_url}?wsdl'
    return SoapClient(wsdl_url)



def test_wsdl_metadata(ws):
    """Test that our server provides valid WSDL metadata."""
    # First check the target namespace is correct. This will fail when you change the tns in the webservice.py
    assert ws.wsdl.tns == ('tns', 'com.dduenas.Estudiantes')

    # Inspect the service definition
    sd = ws.sd[0]
    assert sd.service.name == 'Estudiantes_Service'
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == 'Estudiantes'

    assert len(svc_port.methods) == 4
    assert len(sd.types) == 10

    def test_service_methods(ws):
        """Test that our server provides the expected service methods."""

    #Prueba para obtener la lista de estudiantes
    response = ws.service.listado()
    assert len(response.Estudiante) >= 2
    assert response.Estudiante[0].nombre == "David"
    assert response.Estudiante[1].nombre == "Juan"

    def test_alta_estudiante(ws):
        """Prueba para agregar un nuevo estudiante."""
    response = ws.service.altaEstudiante("21490541", "Luis", "Quimica" )
    assert response["status"] == "COMPLETED"

    #Prueba para verificar que el nuevo estudiante se agregó a la lista
    m = ws.service.listado()
    assert len(m.Estudiante) >= 3
    assert m.Estudiante[0].nombre == "David"
    assert m.Estudiante[1].nombre == "Juan"
    assert m.Estudiante[2].nombre == "Luis"

    """Prueba para eliminar un estudiante existente."""
    response = ws.service.eliminarEstudiante("21490541")
    assert response["status"] == "COMPLETED"


    """Prueba para modificar un estudiante existente."""
    response = ws.service.modificarEstudiante("21490540", "Diego", "Quimica")
    assert response["status"] == "COMPLETED"

    def test_modificar_estudiante(ws):
        """Prueba para modificar un estudiante inexistente."""
    response = ws.service.modificarEstudiante("123", "Juanito", "Quimica")
    assert response["status"] == "ERROR"

    
    def test_eliminar_estudiante(ws):
        """Elimina un estudiante que no existe mediante su ID."""
    response = ws.service.eliminarEstudiante("147")
    assert response["status"] == "ERROR"






  

   
    



    






    





   


