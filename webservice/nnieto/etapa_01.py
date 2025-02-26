"""Etapa 1 del proyecto de la alcancía de Noe Nieto.

Este módulo contiene la implementación de la etapa 1 del proyecto de la
alcancía.

En la etapa 1 se implementa el servicio web de la alcancía con las siguientes
operaciones: - saldo: Devuelve el saldo actual de la alcancía. - deposito:
Deposita una cantidad en la alcancía y devuelve el nuevo saldo. - retiro: Retira
una cantidad de la alcancía y devuelve el nuevo saldo. - movimientos: Devuelve
la lista de movimientos de la alcancía.

En esta etapa, las operaciones de deposito y retiro simplemente devuelven el
doble y el triple de la cantidad depositada o retirada, respectivamente. No hay
ninguna lógica de negocio en estas operaciones. Solo es el esqueleto de la
alcancía.
"""
from datetime import datetime

from spyne import Application, Array, ComplexModel, DateTime, Decimal, Service, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Movimiento(ComplexModel):
    """Modelo que representa un retiro o un depósito en la alcancía.

    Los depósitos tienen un valor positivo y los retiros un valor negativo.
    """
    fecha = DateTime
    cantidad = Decimal


class AlcanciaService(Service):
    """Este es el servicio web de la alcancía implementado con la librería Spyne."""

    @srpc(_returns=Decimal)
    def saldo():
        """Devuelve el saldo actual de la alcancía. Por el momento siempre devuelve 100."""
        return 100

    @srpc(
        Decimal(gt=0, fraction_digits=0, min_occurs=1, nillable=False), _returns=Decimal,
    )
    def deposito(cantidad):
        """Realiza un depósito en la alcancía y devuelve el nuevo saldo.
        
        En esta etapa solamente devuelve el doble de la cantidad depositada, pero no registra ningún tipo de movimiento.

        Parametros: 
            cantidad -- La cantidad a depositar en la alcancía. Es un número entero positivo, sin fracciones, no puede ser null
        Valor de retorno:
            La cantidad depositada multiplicada por 2. Decimal
        """
        return cantidad * 2

    @srpc(
        Decimal(gt=0, fraction_digits=0, min_occurs=1, nillable=False), _returns=Decimal,
    )
    def retiro(cantidad):
        """Realiza un retiro en la alcancía y devuelve el nuevo saldo.

        En esta etapa solamente devuelve el triple de la cantidad retirada, pero no registra ningún tipo de movimiento.
        Parametros: 
            cantidad -- La cantidad a depositar en la alcancía. Es un número entero positivo, sin fracciones, no puede ser null

        Valor de retorno:
            La cantidad retirada multiplicada por 2. Decimal
        """
        return cantidad * 3

    @srpc(_returns=Array(Movimiento))
    def movimientos():
        """Devuelve la lista de movimientos de la alcancía.
        
        Por el momento siempre devuelve una lista con tres movimientos de prueba.
        """
        return [
            Movimiento(fecha=datetime.strptime("2021-01-01", "%Y-%m-%d"), cantidad=100),
            Movimiento(fecha=datetime.strptime("2021-01-02", "%Y-%m-%d"), cantidad=200),
            Movimiento(fecha=datetime.strptime("2021-01-03", "%Y-%m-%d"), cantidad=300),
        ]


spyne_app = Application(
    services=[AlcanciaService],
    tns="com.noenieto.alcancia",
    name="Alcancia1",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)


wsgi_app = WsgiApplication(spyne_app)
