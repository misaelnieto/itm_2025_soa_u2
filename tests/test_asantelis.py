"""Módulo de pruebas para el servicio SOAP de Animales.

Verifica el correcto funcionamiento de las operaciones CRUD.
"""

from datetime import datetime
from decimal import Decimal

import pytest
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    service_url = f'{base_url}/ws/asantelis/animales'
    wsdl_url = f'{service_url}?wsdl'
    return SoapClient(wsdl_url)


def test_wsdl_metadata(ws):
    """Test that our server provides valid WSDL metadata."""
    # First check the target namespace is correct. This will fail when you change the tns in the webservice.py
    assert ws.wsdl.tns == ("tns", "animales")

    # Inspect the service definition
    sd = ws.sd[0]
    assert sd.service.name == "AnimalService"
    # We have one port, named animalService, that points to the root of the service ...
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == "AnimalService"

    # Has 5 methods, and 13 types
    assert len(svc_port.methods) == 5
    assert len(sd.types) == 12


def test_service_methods(ws):
    """Test that our server provides the expected service methods."""
    # Inicialmente hay 3 animales
    animales = ws.service.listar_animales()
    assert len(animales.Animal) == 3
    assert animales.Animal[0].nombre == "Firulais"
    assert animales.Animal[1].nombre == "Misi"
    assert animales.Animal[2].nombre == "Piolín"

    #Buscar animal por nombre
    animales = ws.service.buscar_nombre("Firulais")
    assert len(animales.Animal) == 1
    assert animales.Animal[0].nombre == "Firulais"
    
    #Agregar animal
    animal = animales.Animal[0]
    animal.nombre = "Firulais"
    animal.especie = "Perro"
    animal.fecha_nacimiento = datetime(2010, 5, 15)
    animal.peso = Decimal("10.5")
    mensaje = ws.service.agregar_animal(animal)
    assert mensaje == "Error: El animal 'Firulais' ya existe."

    animal.nombre = "Firulais2"
    mensaje = ws.service.agregar_animal(animal)
    assert mensaje == "Animal 'Firulais2' agregado exitosamente."
    animales = ws.service.listar_animales()
    assert len(animales.Animal) == 4

    #Eliminar animal agregado (Firulais2)
    mensaje = ws.service.eliminar_animal("Firulais2")
    assert mensaje == "Animal 'Firulais2' eliminado exitosamente."
    animales = ws.service.listar_animales()
    assert len(animales.Animal) == 3

    #Actualizar animal
    animal.nombre = "Firulais"
    animal.especie = "Perro"
    animal.fecha_nacimiento = datetime(2010, 5, 15)
    animal.peso = Decimal("10.5")
    mensaje = ws.service.actualizar_animal(animal)
    assert mensaje == "Animal 'Firulais' actualizado exitosamente."
    animales = ws.service.listar_animales()
    assert len(animales.Animal) == 3
    assert animales.Animal[0].nombre == "Firulais"
    assert animales.Animal[0].especie == "Perro"
    assert animales.Animal[0].fecha_nacimiento == datetime(2010, 5, 15)
    assert animales.Animal[0].peso == Decimal("10.5")

    #Verificar que si se actualizo
    animal.nombre = "Firulais2"
    mensaje = ws.service.actualizar_animal(animal)
    assert mensaje == "Error: El animal 'Firulais2' no existe."
    animales = ws.service.listar_animales()
    assert len(animales.Animal) == 3
    assert animales.Animal[0].nombre == "Firulais"
    assert animales.Animal[0].especie == "Perro"
    assert animales.Animal[0].fecha_nacimiento == datetime(2010, 5, 15)
    assert animales.Animal[0].peso == Decimal("10.5")

    #verificar que no se puede actualizar un animal que no existe
    animal.nombre = "Firulais2"
    mensaje = ws.service.actualizar_animal(animal)
    assert mensaje == "Error: El animal 'Firulais2' no existe."
    animales = ws.service.listar_animales()
    assert len(animales.Animal) == 3
    assert animales.Animal[0].nombre == "Firulais"
    assert animales.Animal[0].especie == "Perro"
    assert animales.Animal[0].fecha_nacimiento == datetime(2010, 5, 15)
    assert animales.Animal[0].peso == Decimal("10.5")
    
    #verificar que no se puede eliminar un animal que no existe
    mensaje = ws.service.eliminar_animal("Firulais2")
    assert mensaje == "Error: El animal 'Firulais2' no existe."
    animales = ws.service.listar_animales()
    assert len(animales.Animal) == 3
    assert animales.Animal[0].nombre == "Firulais"
    assert animales.Animal[0].especie == "Perro"
    assert animales.Animal[0].fecha_nacimiento == datetime(2010, 5, 15)
    assert animales.Animal[0].peso == Decimal("10.5")

