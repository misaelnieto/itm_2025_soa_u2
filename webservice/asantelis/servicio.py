"""Módulo que define el servicio web para gestionar animales.

Operaciones:
    - `listar_animales`: Devuelve la lista de animales existentes.
    - `buscar_nombre`: Busca un animal por nombre.
    - `agregar_animal`: Agrega un nuevo animal a la lista.
    - `eliminar_animal`: Elimina un animal de la lista por nombre.
    - `actualizar_animal`: Modifica los datos de un animal existente.

En esta etapa, las operaciones se realizan sobre una lista en memoria.
En una implementación real, se recomienda utilizar una base de datos para persistencia.
"""

from datetime import datetime

from spyne import Application, Array, ComplexModel, DateTime, Decimal, Service, String, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Animal(ComplexModel):
    """Modelo que representa un animal."""

    nombre = String
    especie = String
    fecha_nacimiento = DateTime
    peso = Decimal


# Lista de animales
animales = [
    Animal(nombre='Firulais', especie='Perro', fecha_nacimiento=datetime(2010, 5, 15), peso=10.5),
    Animal(nombre='Misi', especie='Gato', fecha_nacimiento=datetime(2015, 7, 1), peso=5.2),
    Animal(nombre='Piolín', especie='Canario', fecha_nacimiento=datetime(2018, 3, 20), peso=0.1),
]


class AnimalService(Service):
    """Servicio Web que expone los datos de los animales."""

    @srpc(_returns=Array(Animal))
    def listar_animales():
        """Devuelve la lista de animales."""
        return animales

    @srpc(String, _returns=Array(Animal))
    def buscar_nombre(nombre):
        """Devuelve la lista de animales con un nombre específico."""
        return [a for a in animales if a.nombre == nombre]

    @srpc(Animal, _returns=String)
    def agregar_animal(animal):
        """Agrega un nuevo animal si no existe ya."""
        if any(a.nombre == animal.nombre for a in animales):
            return f"Error: El animal '{animal.nombre}' ya existe."
        animales.append(animal)
        return f"Animal '{animal.nombre}' agregado exitosamente."

    @srpc(String, _returns=String)
    def eliminar_animal(nombre):
        """Elimina un animal si existe."""
        for a in animales:
            if a.nombre == nombre:
                animales.remove(a)
                return f"Animal '{nombre}' eliminado exitosamente."
        return f"Error: El animal '{nombre}' no existe."

    @srpc(Animal, _returns=String)
    def actualizar_animal(animal):
        """Actualiza un animal si existe."""
        for i, a in enumerate(animales):
            if a.nombre == animal.nombre:
                animales[i] = animal
                return f"Animal '{animal.nombre}' actualizado exitosamente."
        return f"Error: El animal '{animal.nombre}' no existe."


# Configuración del servicio
spyne_app = Application(
    services=[AnimalService],
    tns='animales',
    name='AnimalService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(validator='lxml'),
)

wsgi_app = WsgiApplication(spyne_app)
