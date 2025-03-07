"""Módulo que define el servicio web para la gestión de eventos en el sistema.

Este servicio permite realizar operaciones relacionadas con eventos, incluyendo:
    - `listado`: Devuelve la lista de todos los eventos registrados.
    - `crear_evento`: Crea un nuevo evento con nombre y descripción.
    - `leer_evento`: Recupera los datos de un evento dado su nombre.
    - `actualizar_evento`: Modifica la descripción de un evento existente.
    - `eliminar_evento`: Elimina un evento por su nombre.

Los eventos son almacenados en un diccionario en memoria.
"""

# Importación de librerías necesarias de Spyne para crear un servicio web SOAP
from spyne import Application, Array, ComplexModel, Service, String, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Evento(ComplexModel):
    """Modelo que representa un evento.
    
    Atributos:
        nombre -- Nombre del evento.
        descripcion -- Breve descripción del evento.
    """
    nombre = String
    descripcion = String

class EventosService(Service):
    """Servicio web para la gestión de eventos."""

    # Diccionario en memoria que almacena los eventos registrados
    eventos = {
        "Boda": Evento(nombre="Boda", descripcion="Se casan"),
        "XV años": Evento(nombre="XV años", descripcion="Fiesta"),
        "Bautizo": Evento(nombre="Bautizo", descripcion="Borrachera"),
    }

    @srpc(_returns=Array(Evento))
    def listado():
        """Devuelve la lista de eventos existentes.
        
        Retorno:
            Lista de objetos Evento con nombre y descripción.
        """
        return list(EventosService.eventos.values())

    @srpc(String, String, _returns=String)
    def crear_evento(nombre, descripcion):
        """Crea un nuevo evento y lo agrega a la lista.

        Parámetros:
            nombre -- Nombre único del evento a crear.
            descripcion -- Breve descripción del evento.
        
        Retorno:
            Un mensaje indicando si el evento fue creado o si ya existía.
        """
        if nombre in EventosService.eventos:
            return "Evento ya existe"
        EventosService.eventos[nombre] = Evento(nombre=nombre, descripcion=descripcion)
        return "Evento creado exitosamente"

    @srpc(String, _returns=Evento)
    def leer_evento(nombre):
        """Recupera la información de un evento dado su nombre.

        Parámetros:
            nombre -- Nombre del evento a consultar.
        
        Retorno:
            Un objeto Evento si existe, de lo contrario None.
        """
        return EventosService.eventos.get(nombre, None)

    @srpc(String, String, _returns=String)
    def actualizar_evento(nombre, descripcion):
        """Modifica la descripción de un evento existente.

        Parámetros:
            nombre -- Nombre del evento a modificar.
            descripcion -- Nueva descripción del evento.
        
        Retorno:
            Un mensaje indicando si el evento fue actualizado o no existe.
        """
        if nombre in EventosService.eventos:
            EventosService.eventos[nombre] = Evento(nombre=nombre, descripcion=descripcion)
            return "Evento actualizado exitosamente"
        return "Evento no existe"

    @srpc(String, _returns=String)
    def eliminar_evento(nombre):
        """Elimina un evento dado su nombre.

        Parámetros:
            nombre -- Nombre del evento a eliminar.
        
        Retorno:
            Un mensaje indicando si el evento fue eliminado o si no existía.
        """
        if nombre in EventosService.eventos:
            del EventosService.eventos[nombre]
            return "Evento eliminado exitosamente"
        return "Evento no existe"

# Configuración de la aplicación SOAP utilizando el protocolo SOAP 1.1
spyne_app = Application(
    services=[EventosService],  # Lista de servicios disponibles
    tns="com.imayo.eventos",  # Espacio de nombres del servicio
    name="Eventos",  # Nombre del servicio
    in_protocol=Soap11(validator="lxml"),  # Protocolo de entrada SOAP 1.1
    out_protocol=Soap11(validator="lxml"),  # Protocolo de salida SOAP 1.1
)

# Creación de la aplicación WSGI que envuelve la aplicación SOAP
wsgi_app = WsgiApplication(spyne_app)


