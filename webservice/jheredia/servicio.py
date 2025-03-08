"""Este módulo contiene la implementación del servicio SOAP para el manejo de ciudades.

Incluye operaciones como listado, registro, eliminación y actualización de datos de ciudades.
"""


from spyne import Application, Array, ComplexModel, Service, String, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Ciudad(ComplexModel):
    """Clase que representa una ciudad con nombre, país y población."""
    nombre = String
    pais = String
    poblacion = String

# Lista inicial de ciudades se puede agregar mas aqui o desde soap ui
_ciudades = [
    Ciudad(nombre="Mexicali", pais="México", poblacion="1,000,000"),
    Ciudad(nombre="Tijuana", pais="México", poblacion="2,000,000"),
]


class CiudadesService(Service):
    """Servicio SOAP que permite realizar operaciones CRUD sobre ciudades."""

    @srpc(_returns=Array(Ciudad))
    def listado():
        """Obtiene la lista de ciudades disponibles."""
        return _ciudades

    @srpc(String, String, String, _returns=String)
    def registrar(nombre, pais, poblacion):
        """Registra una nueva ciudad con nombre, país y población."""
        _ciudades.append(Ciudad(nombre=nombre, pais=pais, poblacion=poblacion))
        return "Ciudad registrada"

    @srpc(String, _returns=String)
    def eliminar(nombre):
        """Elimina una ciudad por su nombre. Retorna un mensaje de éxito o error."""
        global _ciudades
        ciudades_filtradas = [c for c in _ciudades if c.nombre != nombre]

        if len(ciudades_filtradas) == len(_ciudades):
            return "Ciudad no encontrada"

        _ciudades = ciudades_filtradas
        return "Ciudad eliminada correctamente"

    @srpc(String, String, String, _returns=String)
    def actualizar(nombre, nuevo_pais, nueva_poblacion):
        """Actualiza el país y población de una ciudad existente."""
        for ciudad in _ciudades:
            if ciudad.nombre == nombre:
                ciudad.pais = nuevo_pais
                ciudad.poblacion = nueva_poblacion
                return "Ciudad actualizada correctamente"
        return "Ciudad no encontrada"


# Configuración del WebService
spyne_app = Application(
    services=[CiudadesService],
    tns="com.jheredia.ciudades",
    name="Ciudades",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)
