"""Este módulo contiene el CRUD de nuestro webservice Libreria.

Operaciones:
    - `listado`: Devuelve la lista de libros existentes.
    - `buscar`: Busca un libro ya sea por titulo o ISBN.
    - `agregar`: Agrega un libro a la lista.
    - `eliminar`: Elimina un libro de la lista por titulo o ISBN.
    - `actualizar`: Modifica los datos de un libro existente mediante su ISBN.

En esta etapa, las operaciones se realizan sobre una lista en memoria.
En una implementacion real, se recomienda utilizar una base de datos para persistencia.
"""

from spyne import (
    AnyDict,
    Application,
    Array,
    ComplexModel,
    Integer,
    Service,
    String,
    srpc,
)
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Libro(ComplexModel):
    """Modelo de datos que representa un libro en la libreria."""

    titulo = String
    autor = String
    ISBN = Integer


# Lista de libros (almacenamiento temporal en memoria)
libros = [
    Libro(titulo="El señor de los anillos", autor="J.R.R. Tolkien", ISBN=12345),
    Libro(titulo="El hobbit", autor="J.R.R. Tolkien", ISBN=34567),
]


class LibreriaService(Service):
    """Servicio web que expone las operaciones CRUD de la libreria."""

    @srpc(_returns=Array(Libro))
    def listado():
        """Devuelve la lista de libros existentes en la libreria."""
        return libros

    @srpc(String, Integer, _returns=AnyDict)
    def buscar(titulo, isbn):
        """Busca un libro por titulo o ISBN y retorna el que haga match."""
        if titulo is None and isbn is None:
            return {"status": "ERROR", "mensaje": "Debe especificar titulo o ISBN"}
        for libro in libros:
            if libro.titulo.lower() == titulo.lower() or isbn == libro.ISBN:
                return {
                    "titulo": libro.titulo,
                    "autor": libro.autor,
                    "ISBN": libro.ISBN,
                    "status": "OK",
                }
        return {"status": "ERROR", "mensaje": "Libro no encontrado"}

    @srpc(
        String(min_len=5, nillable=False, min_occurs=1),
        String(min_len=5, nillable=False),
        Integer(nillable=False),
        _returns=AnyDict,
    )
    def agregar(titulo, autor, isbn):
        """Agrega un nuevo libro a la lista."""
        for libro in libros:
            if isbn == libro.ISBN:
                return {"status": "ERROR", "mensaje": "El ISBN ya existe"}
        libros.append(Libro(titulo=titulo, autor=autor, ISBN=isbn))
        return {"titulo": titulo, "autor": autor, "ISBN": isbn, "status": "OK"}

    @srpc(String(nillable=False), Integer(nillable=False), _returns=AnyDict)
    def eliminar(titulo, isbn):
        """Elimina un libro por titulo o ISBN."""
        for i, libro in enumerate(libros):
            if libro.titulo == titulo or isbn == libro.ISBN:
                libros.pop(i)
                return {"status": "OK", "mensaje": "Libro eliminado"}
        return {"status": "ERROR", "mensaje": "Libro no encontrado"}

    @srpc(
        Integer(nillable=False),
        String(nillable=False),
        String(nillable=False),
        _returns=AnyDict,
    )
    def actualizar(isbn, nuevo_titulo, nuevo_autor):
        """Modifica los datos de un libro existente mediante su ISBN."""
        for libro in libros:
            if isbn == libro.ISBN:
                libro.titulo = nuevo_titulo
                libro.autor = nuevo_autor
                return {"status": "OK", "mensaje": "Libro actualizado"}
        return {"status": "ERROR", "mensaje": "Libro no encontrado"}


# Configuracion del servicio SOAP
spyne_app = Application(
    services=[LibreriaService],
    tns="libreria",
    name="LibreriaService",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)
