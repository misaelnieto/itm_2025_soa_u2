"""Etapa 2 del proyecto de la alcancía de Noe Nieto.

Este módulo contiene la implementación de la etapa 2 del servicio web Alcancía.

En esta etapa aún no se persisten los datos en una base de datos, sino que los
movimientos se guardan en una lista en memoria. Esto nos permite simular fácilmente
el comportamiento de la alcancía sin tener que preocuparnos por la persistencia de los datos.

Cambios con respecto a la versión 1:

- Se agregaron validaciones a los parámetros de las operaciones de depósito y retiro.
- Se define una clase Resultado para representar el resultado de las operaciones de depósito y retiro.
- Se cambió el tipo de retorno de las operaciones de depósito y retiro a Resultado.
- Se agregó la operación movimientos que devuelve la lista de movimientos de la alcancía.

"""
from datetime import datetime

from spyne import Application, Array, ComplexModel, DateTime, Decimal, Service, Unicode, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

_movimientos_db = []

def _saldo():
    return sum([m.cantidad for m in _movimientos_db])


class Movimiento(ComplexModel):
    """Modelo que representa un retiro o un depósito en la alcancía.

    Los depósitos tienen un valor positivo y los retiros un valor negativo.
    """
    fecha = DateTime
    cantidad = Decimal


class Resultado(ComplexModel):
    """Representa el resultado de una operación de depósito o retiro. Opcionalmente incluye el saldo actual."""
    status = Unicode
    message = Unicode
    saldo = Decimal

    @classmethod
    def ok(cls, mensaje, nuevo_saldo):
        """Crea un objeto Resultado con status 'OK', un mensaje y el saldo actual."""
        return cls(status='OK', message=mensaje, saldo=nuevo_saldo)
    
    @classmethod
    def error(cls, mensaje):
        """Crea un objeto Resultado con status 'ERROR' y un mensaje."""
        return cls(status='ERROR', message=mensaje)


class AlcanciaService(Service):
    """Este es el servicio web de la alcancía implementado con la librería Spyne."""

    @srpc(_returns=Decimal)
    def saldo():
        """Devuelve el saldo actual de la alcancía como un número decimal."""
        return _saldo()

    @srpc(
        Decimal(gt=0, fraction_digits=2, min_occurs=1, nillable=False), _returns=Resultado,
    )
    def deposito(cantidad):
        """Realiza un depósito en la alcancía y devuelve el nuevo saldo.
        
        Parametros:
            cantidad -- La cantidad a depositar en la alcancía. Es un número decimal positivo, con dos decimales, no puede ser null
        
        Valor de retorno:
            Un objeto Resultado con el resultado de la operación y el saldo actual.
        """
        _movimientos_db.append(Movimiento(fecha=datetime.now(), cantidad=cantidad))
        return Resultado.ok("Deposito exitoso", _saldo())

    @srpc(
        Decimal(gt=0, fraction_digits=2, min_occurs=1, nillable=False), _returns=Resultado,
    )
    def retiro(cantidad):
        """Realiza un retiro en la alcancía y devuelve el nuevo saldo.

        Si se intenta retirar más dinero del que hay en la alcancía, la
        operación falla y se devuelve un mensaje de Resultado.error(). Si el
        retiro es exitoso, se registra un movimiento con la cantidad negativa.
        
        Parametros:
            cantidad -- La cantidad a retirar de la alcancía. Es un número decimal positivo, con dos decimales, no puede ser null
            
        Valor de retorno:
            Un objeto Resultado con el resultado de la operación y el saldo actual.
        """
        if cantidad > _saldo():
            return Resultado.error("Fondos insuficientes")
        _movimientos_db.append(Movimiento(fecha=datetime.now(), cantidad=-cantidad))
        return Resultado.ok("Retiro exitoso", _saldo())

    @srpc(_returns=Array(Movimiento))
    def movimientos():
        """Devuelve la lista de movimientos de la alcancía.

        Valor de retorno:
            Un arreglo de objetos Movimiento.
        """
        return _movimientos_db


spyne_app = Application(
    services=[AlcanciaService],
    tns="com.noenieto.alcancia",
    name="Alcancia2",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)


wsgi_app = WsgiApplication(spyne_app)
