from spyne import Service, srpc, AnyDict, String, ComplexModel, Array, Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Perrito(ComplexModel):
    nombre = String
    raza = String


class PerritosService(Service):
    @srpc(_returns=Array(Perrito))
    def listado():
        return [
            Perrito(nombre="Lucy", raza="Cocker"),
            Perrito(nombre="Mushu", raza="Husky"),
            Perrito(nombre="Luna", raza="Labrador"),
            Perrito(nombre="Firulais", raza="Mixta"),
        ]

    @srpc(String, String, _returns=String,)
    def registrar(nombre, raza):
        return "OK"
    
    @srpc(String, _returns=String)
    def eliminar(nombre):
        return "OK"
    
    @srpc(String, String, _returns=String)
    def editar(nombre, nueva_raza):
        return "OK"


spyne_app = Application(
    services=[PerritosService],
    tns='com.ffernandez.perritos',
    name='Perritos',
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)
