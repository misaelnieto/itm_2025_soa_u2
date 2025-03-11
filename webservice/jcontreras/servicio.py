"""Este módulo contiene la implementación del servicio SOAP para el manejo de ventas.

Incluye operaciones como listado, registro, eliminación y actualización de ventas.
"""

from spyne import Application, Array, ComplexModel, Float, Service, String, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Venta(ComplexModel):
    """Clase que representa una venta con producto, cantidad, precio y total.""" 
    producto = String
    cantidad = Float
    precio = Float
    total = Float


# Lista inicial de ventas, se puede agregar más aquí o desde SoapUI
_ventas = [
    Venta(producto="Laptop", cantidad=1, precio=1500.00, total=1500.00),
    Venta(producto="Teléfono", cantidad=2, precio=500.00, total=1000.00),
]


class VentasService(Service):
    """Servicio SOAP que permite realizar operaciones CRUD sobre ventas."""

    @srpc(_returns=Array(Venta))
    def listado():
        """Obtiene la lista de ventas realizadas."""
        return _ventas

    @srpc(String, Float, Float, _returns=String)
    def registrar(producto, cantidad, precio):
        """Registra una nueva venta con producto, cantidad y precio.""" 
        total = cantidad * precio
        _ventas.append(Venta(producto=producto, cantidad=cantidad, precio=precio, total=total))
        return "Venta registrada"

    @srpc(String, _returns=String)
    def eliminar(producto):
        """Elimina una venta por el nombre del producto. Retorna un mensaje de éxito o error.""" 
        global _ventas
        ventas_filtradas = [v for v in _ventas if v.producto != producto]

        if len(ventas_filtradas) == len(_ventas):
            return "Venta no encontrada"

        _ventas = ventas_filtradas
        return "Venta eliminada correctamente"

    @srpc(String, Float, Float, _returns=String)
    def actualizar(producto, nuevo_precio, nueva_cantidad):
        """Actualiza el precio y la cantidad de una venta existente.""" 
        for venta in _ventas:
            if venta.producto == producto:
                venta.precio = nuevo_precio
                venta.cantidad = nueva_cantidad
                venta.total = nueva_cantidad * nuevo_precio
                return "Venta actualizada correctamente"
        return "Venta no encontrada"


# Configuración del WebService
spyne_app = Application(
    services=[VentasService],
    tns="com.jcontreras.ventas",
    name="Ventas",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)
