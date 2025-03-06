from spyne import Service, srpc, String, ComplexModel, Array, Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

#  Clase que representa un producto
class Producto(ComplexModel):
    nombre = String
    categoria = String  

#  Lista inicial de productos
_productos = [
    Producto(nombre="Coca-cola", categoria="Refresco"),
    Producto(nombre="Sabritas", categoria="Fritura"),
]

#  Servicio SOAP con los métodos CRUD
class ProductosService(Service):
    
    #  Método para obtener la lista de productos
    @srpc(_returns=Array(Producto))
    def listado():
        return _productos 

    #  Método para registrar un nuevo producto
    @srpc(String, String, _returns=String)
    def registrar(nombre, categoria):
        _productos.append(Producto(nombre=nombre, categoria=categoria))
        return "Producto registrado"

    #  Método para eliminar un producto por su nombre
    @srpc(String, _returns=String)
    def eliminar(nombre):
        global _productos
        productos_filtrados = [p for p in _productos if p.nombre != nombre]
        
        if len(productos_filtrados) == len(_productos):
            return "Producto no encontrado"
        
        _productos = productos_filtrados
        return "Producto eliminado correctamente"

    #  Método para editar la categoría de un producto
    @srpc(String, String, _returns=String)
    def editar(nombre, nueva_categoria):
        for producto in _productos:
            if producto.nombre == nombre:
                producto.categoria = nueva_categoria
                return "Producto actualizado correctamente"
        return "Producto no encontrado"

#  Configuración del WebService
spyne_app = Application(
    services=[ProductosService],
    tns='com.dramos.productos',
    name='Productos',
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)
