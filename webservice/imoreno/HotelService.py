"""Este módulo implementa el servicio de registro de clientes en un hotel.

- listaClientes: Este método devuelve la lista de clientes registrados en el hotel
- RegistroCliente: Este tiene un método que permite registrar un cliente en el hotel.
- BuscarCliente: Este método permite buscar un cliente en el hotel.
- BorrarCliente: Este método permite borrar un cliente del hotel.
- ModificarCliente: Este método permite modificar la información de un cliente en el hotel.
"""  # noqa: D205
from spyne import Application, ComplexModel, Integer, Service, Unicode, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Cliente(ComplexModel):
    """Modelo que representa una entrada de cliente al hotel."""
    nombre = Unicode
    ap_primero = Unicode
    ap_segundo = Unicode
    num_habitación = Integer

_clientes_db = [Cliente(nombre='Juan', ap_primero='Perez', ap_segundo='Gomez', num_habitación=101),
                   Cliente(nombre='Pedro', ap_primero='Gomez', ap_segundo='Perez', num_habitación=102)]

class Resultado(ComplexModel):
    """Representa el resultado de una transacción."""
    status = Unicode
    message = Unicode

    @classmethod
    def ok(cls, mensaje):
        """Crea un objeto Resultado con status 'OK' y un mensaje."""
        return cls(status='OK', message=mensaje)
    
    @classmethod
    def error(cls, mensaje):
        """Crea un objeto Resultado con status 'ERROR' y un mensaje."""
        return cls(status='ERROR', message=mensaje)


class HotelService(Service):
    """Este es el servicio web del registro del hotel implementado con la librería Spyne."""

    @srpc(_returns=ComplexModel)
    def listaClientes():
        """Devuelve el listado de clientes registrados."""
        return _clientes_db

    @srpc(Unicode, Unicode, Unicode, Integer, _returns=Resultado)
    def RegistroCliente(nombre, ap_primero, ap_segundo, num_habitacion):
        """Realiza un registro de un cliente en el hotel y devuelve el nuevo saldo.
        
        Parametros:
            nombre -- El nombre del cliente
            ap_primero -- El primer apellido del cliente
            ap_segundo -- El segundo apellido del cliente
        Valor de retorno:
            Un objeto Resultado con el resultado de la operación y el saldo actual.
        """
        if _clientes_db.append(Cliente(nombre=nombre, ap_primero=ap_primero, ap_segundo=ap_segundo, num_habitacion=num_habitacion)):
            return Resultado.ok(_clientes_db)
        return Resultado.error("Error al registrar el cliente")

    @srpc(Unicode, Unicode, Unicode, _returns=Resultado)
    def BuscarCliente(nombre, ap_primero, ap_segundo):
        """Busca un cliente en el hotel y devuelve su información.

        - nombre -- El nombre del cliente
        - ap_primero -- El primer apellido del cliente
        - ap_segundo -- El segundo apellido del cliente
        - Valor de retorno:
            Un objeto Resultado con el resultado de la operación y la información del cliente.
        """
        for cliente in _clientes_db:
            if cliente.nombre == nombre and cliente.ap_primero == ap_primero and cliente.ap_segundo == ap_segundo:
                return Resultado.ok({cliente})
        return Resultado.error("Cliente no encontrado")

    @srpc(Unicode, Unicode, Unicode, _returns=Resultado)
    def BorrarCliente(nombre, ap_primero, ap_segundo):
        """Borra un cliente del hotel."""
        for cliente in _clientes_db:
            if cliente.nombre == nombre and cliente.ap_primero == ap_primero and cliente.ap_segundo == ap_segundo:
                _clientes_db.remove(cliente)
                return Resultado.ok(_clientes_db)
        return Resultado.error("Cliente no encontrado")
    
    @srpc(Unicode, Unicode, Unicode, Integer, _returns=Resultado)
    def ModificarCliente(nombre, ap_primero, ap_segundo, num_habitacion):
        """Modifica la información de un cliente en el hotel."""
        for cliente in _clientes_db:
            if cliente.nombre == nombre and cliente.ap_primero == ap_primero and cliente.ap_segundo == ap_segundo:
                cliente.num_habitacion = num_habitacion
                return Resultado.ok(_clientes_db)
        return Resultado.error("Cliente no encontrado")

spyne_app = Application(
    services=[HotelService],
    tns="com.imoreno.HotelService",
    name="HotelService",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)


wsgi_app = WsgiApplication(spyne_app)
