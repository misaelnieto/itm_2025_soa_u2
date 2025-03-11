
"""Este módulo contiene el CRUD del webservice de Gestión de Cursos.

Operaciones:
    - 'listado_cursos': Devuelve la lista de los cursos existentes.
    - 'buscar_curso': Busca un curso por su nombre o ID.
    - 'agregar_curso': Agrega un nuevo curso.
    - 'eliminar_curso': Elimina un curso de la lista por su nombre o ID.
    - 'actualizar_curso': Modifica los datos de un curso existente mediante su ID.

En esta etapa, las operaciones se realizan sobre una lista en memoria.
En una implementación real, se recomienda utilizar una base de datos para persistencia.
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


class Curso(ComplexModel):
    """Modelo de datos que representa un curso en el sistema de gestión de cursos."""

    id_curso = Integer
    nombre = String
    profesor = String


# Lista de cursos (almacenamiento temporal en memoria)
cursos = [
    Curso(id_curso=1, nombre="Programación en Python", profesor="Noe Nieto"),
    Curso(id_curso=2, nombre="Bases de Datos SQL", profesor="Marisela Ponce"),
    Curso(id_curso=3, nombre="Inteligencia Artificial", profesor="Jaime Olvera"),
    Curso(id_curso=4, nombre="Taller de Sistemas Operativos", profesor="Mario Chong"),
]


class CursoService(Service):
    """Servicio web que expone las operaciones CRUD de la gestión de cursos."""

    @srpc(_returns=Array(Curso))
    def listado_cursos():
        """Devuelve la lista de cursos existentes en el sistema."""
        return cursos

    @srpc(String, Integer, _returns=AnyDict)
    def buscar_curso(nombre, id_curso):
        """Busca un curso por su nombre o ID y retorna el que haga match."""
        if not nombre and not id_curso:
            return {"status": "ERROR", "mensaje": "Debe especificar nombre o ID"}
        for curso in cursos:
            if curso.nombre.lower() == nombre.lower() or id_curso == curso.id_curso:
                return {
                    "id_curso": curso.id_curso,
                    "nombre": curso.nombre,
                    "profesor": curso.profesor,
                    "status": "OK",
                }
        return {"status": "ERROR", "mensaje": "Curso no encontrado"}

    @srpc(
        Integer(nillable=False),
        String(min_len=5, nillable=False),
        String(min_len=5, nillable=False),
        _returns=AnyDict,
    )
    def agregar_curso(id_curso, nombre, profesor):
        """Agrega un nuevo curso a la lista."""
        for curso in cursos:
            if id_curso == curso.id_curso:
                return {"status": "ERROR", "mensaje": "El ID del curso ya existe"}
        cursos.append(Curso(id_curso=id_curso, nombre=nombre, profesor=profesor))
        return {"id_curso": id_curso, "nombre": nombre, "profesor": profesor, "status": "OK"}

    @srpc(String(nillable=False), Integer(nillable=False), _returns=AnyDict)
    def eliminar_curso(nombre, id_curso):
        """Elimina un curso por nombre o ID."""
        for i, curso in enumerate(cursos):
            if curso.nombre == nombre or id_curso == curso.id_curso:
                cursos.pop(i)
                return {"status": "OK", "mensaje": "Curso eliminado"}
        return {"status": "ERROR", "mensaje": "Curso no encontrado"}

    @srpc(
        Integer(nillable=False),
        String(nillable=False),
        String(nillable=False),
        _returns=AnyDict,
    )
    def actualizar_curso(id_curso, nuevo_nombre, nuevo_profesor):
        """Modifica los datos de un curso existente mediante su ID."""
        for curso in cursos:
            if id_curso == curso.id_curso:
                curso.nombre = nuevo_nombre
                curso.profesor = nuevo_profesor
                return {"status": "OK", "mensaje": "Curso actualizado"}
        return {"status": "ERROR", "mensaje": "Curso no encontrado"}



# Configuración del servicio SOAP
spyne_app = Application(
    services=[CursoService],
    tns="gestorcursos",
    name="CursoService",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)
