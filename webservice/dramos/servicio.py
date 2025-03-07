
"""Módulo que implementa un servicio SOAP para gestionar productos.

Proporciona métodos para listar, registrar, eliminar y actualizar productos.
"""

from spyne import Application, Array, ComplexModel, Service, String, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Producto(ComplexModel):
    """Clase que representa un producto con nombre, categoría y precio."""

    nombre = String
    categoria = String
    precio = String


# Lista inicial de productos con precio
_productos = [
    Producto(nombre="Coca-cola", categoria="Refresco", precio="15"),
    Producto(nombre="Sabritas", categoria="Fritura", precio="10"),
]


class ProductosService(Service):
    """Servicio SOAP que permite realizar operaciones CRUD sobre productos."""

    @srpc(_returns=Array(Producto))
    def listado():
        """Obtiene la lista de productos disponibles."""
        return _productos

    @srpc(String, String, String, _returns=String)
    def registrar(nombre, categoria, precio):
        """Registra un nuevo producto con nombre, categoría y precio."""
        _productos.append(Producto(nombre=nombre, categoria=categoria, precio=precio))
        return "Producto registrado"

    @srpc(String, _returns=String)
    def eliminar(nombre):
        """Elimina un producto por su nombre. Retorna un mensaje de éxito o error."""
        global _productos
        productos_filtrados = [p for p in _productos if p.nombre != nombre]

        if len(productos_filtrados) == len(_productos):
            return "Producto no encontrado"

        _productos = productos_filtrados
        return "Producto eliminado correctamente"

    @srpc(String, String, String, _returns=String)
    def actualizar(nombre, nueva_categoria, nuevo_precio):
        """Actualiza la categoría y precio de un producto existente."""
        for producto in _productos:
            if producto.nombre == nombre:
                producto.categoria = nueva_categoria
                producto.precio = nuevo_precio
                return "Producto actualizado correctamente"
        return "Producto no encontrado"


# Configuración del WebService
spyne_app = Application(
    services=[ProductosService],
    tns="com.dramos.productos",
    name="Productos",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)
