"""Este módulo contiene la implementación del servicio SOAP para el manejo de carros.

Incluye operaciones como listado, registro, eliminación y actualización de datos de carros.
"""


from spyne import Application, Array, ComplexModel, Service, String, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Carro(ComplexModel):
    """Clase que representa un carro con marca, modelo y año."""
    marca = String
    modelo = String
    año = String

# Lista inicial de carros
_carros = [
    Carro(marca="Toyota", modelo="Corolla", año="2020"),
    Carro(marca="Nissan", modelo="Sentra", año="2019"),
]


class CarrosService(Service):
    """Servicio SOAP que permite realizar operaciones CRUD sobre carros."""

    @srpc(_returns=Array(Carro))
    def listado():
        """Obtiene la lista de carros disponibles."""
        return _carros

    @srpc(String, String, String, _returns=String)
    def registrar(marca, modelo, año):
        """Registra un nuevo carro con marca, modelo y año."""
        _carros.append(Carro(marca=marca, modelo=modelo, año=año))
        return "Carro registrado"

    @srpc(String, String, _returns=String)
    def eliminar(marca, modelo):
        """Elimina un carro por su marca y modelo. Retorna un mensaje de éxito o error."""
        global _carros
        carros_filtrados = [c for c in _carros if c.marca != marca or c.modelo != modelo]

        if len(carros_filtrados) == len(_carros):
            return "Carro no encontrado"

        _carros = carros_filtrados
        return "Carro eliminado correctamente"

    @srpc(String, String, String, _returns=String)
    def actualizar(marca, modelo, nuevo_año):
        """Actualiza el año de un carro existente."""
        for carro in _carros:
            if carro.marca == marca and carro.modelo == modelo:
                carro.año = nuevo_año
                return "Carro actualizado correctamente"
        return "Carro no encontrado"  # Línea que se utiliza cuando no se encuentra el carro


# Configuración del WebService
spyne_app = Application(
    services=[CarrosService],
    tns="com.fcalzada.carros",
    name="Carros",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)
