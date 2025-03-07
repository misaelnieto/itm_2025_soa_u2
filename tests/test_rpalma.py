"""Test del webservice de contactos."""

import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
     """Inicializar un cliente SOAP para el servidor WSGI."""
     base_url = wsgi_live_server
     service_url = f"{base_url}/ws/rpalma/contactos"
     wsdl_url = f"{service_url}?wsdl"
     return SoapClient(wsdl_url)

def test_wsdl_metadata(ws):
    """Verificar que nuestro servicio tiene metadatos validos."""
    # Verificar que el namespace sea correcto en el webservice.
    assert ws.wsdl.tns == ("tns", "com.rpalma.contactos")

    # Verifica la definicion del servicio 
    sd = ws.sd[0]
    assert sd.service.name == "ContactosService"
    # Verificar el puerto de nuestro servicio 
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == "Contactos"

    # Has 5 methods, and 16 types
    assert len(svc_port.methods) == 5
    assert len(sd.types) == 15
    
def test_service_methods(ws):
    """Probar el comportamiento de los metodos de nuestro servicio."""
    # Se inicializa la agenda con 4 contactos
    contact = ws.service.lista()
    assert len(contact.Contacto) == 4
    assert contact.Contacto[0].nombre == "Jair"
    assert contact.Contacto[1].nombre == "Elena"
    assert contact.Contacto[2].nombre == "Mariela"
    assert contact.Contacto[3].nombre == "Diego"

    # Agregando un contacto
    contact = ws.service.agregar("persona", "4567891", "correo de prueba")
    assert contact.status =="OK"
    assert contact.nombre == "persona"
    assert contact.telefono == "4567891"
    assert contact.correo == "correo de prueba"
    
    #probando con un telefono repetido
    contact = ws.service.agregar("persona2", "6868912345", "correo de prueba")
    assert contact.status =="ERROR"
    
    #probando con un correo repetido
    contact = ws.service.agregar("persona2", "6543219874", "diego@itmexicali.edu.mx")
    assert contact.status =="ERROR"
    
    #Verificar que se agrego
    contact = ws.service.lista()
    assert len(contact.Contacto) == 5 
    assert contact.Contacto[4].nombre == "persona"
    
    # Buscamos un contacto que existe
    contact = ws.service.buscar("Elena")
    assert contact.status =="OK"
    
    # Buscamos un contacto que no existe
    contact = ws.service.buscar("Maria")
    assert contact.status =="ERROR"

    # Editar un contacto
    contact = ws.service.editar(3,"Marco","6863215612", "otro correo")
    assert contact.status == "OK"
    assert int(contact.num)== 3
    assert contact.nombre=="Marco"
    assert contact.telefono == "6863215612"
    assert contact.correo == "otro correo"
    
    contact = ws.service.editar(None,"Marco","6863215612", "otro correo") #enviando int vacio
    assert contact.status == "ERROR"
    
    contact = ws.service.editar(8,"Marco","6863215612", "otro correo") #enviando num identificador que no existe
    assert contact.status == "ERROR"
    
    
    #Eliminar un contacto
    contact = ws.service.eliminar(4)
    assert contact.status == "OK"
    contact = ws.service.lista()
    assert len(contact.Contacto) == 4 #verificar que se elimino
    
    contact = ws.service.eliminar(6) #enviar num que no esta en la agneda
    assert contact.status == "ERROR"
    
    contact = ws.service.eliminar(None) #enviar None
    assert contact.status == "ERROR"
