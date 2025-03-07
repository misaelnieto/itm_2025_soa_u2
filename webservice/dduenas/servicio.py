"""Este modulo contiene la etapa 1 del proyecto Estudiantes.
 
Operaciones:
        `listado`:  Devuelve la lista de estudiantes registrados actualmente.
        `altaEstudiante`: Agrega un nuevo estudiante a la lista.
        `eliminarEstudiante`: Elimina un estudiante por su ID.
        `modificarEstudiante`: Modifica los datos de un estudiante existente en la lista mediante su ID.

En esta etapa, las operaciones para la alta, baja y modificación de información de los alumnos se puede manipular correctamente.

"""

from spyne import AnyDict, Application, Array, ComplexModel, Service, String, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Estudiante(ComplexModel):
    """Modelo que representa los atributos que poseen los estudiantes."""
    nombre = String
    id = String
    carrera = String

# Listado de estudiantes predefinidos
estudiantes = [
    Estudiante(nombre="David", id="21490540", carrera="Sistemas"),
    Estudiante(nombre="Juan", id="21490539", carrera="Sistemas"),
]


class Estudiantes_Service(Service):
    """Este es el servicio web del proyecto Estudiantes."""

    @srpc(_returns=Array(Estudiante))
    def listado():
        """Devuelve la lista de estudiantes registrados actualmente."""
        return estudiantes

    # Método para agregar estudiantes a la lista
    @srpc(String, String, String, _returns=AnyDict)
    def altaEstudiante(id, nombre, carrera):  # noqa: A002
        """Agrega un nuevo estudiante a la lista."""
        estudiantes.append(Estudiante(id=id, nombre=nombre, carrera=carrera))
        return {"status": "COMPLETED", "mensaje": "Estudiante agregado correctamente"}

    # Método para eliminar estudiantes mediante su ID
    @srpc(String(nillable=False), _returns=AnyDict)
    def eliminarEstudiante(id):  # noqa: A002
        """Elimina un estudiante por su ID."""
        """En esta sección se elimina el estudiante completamente con solamente ingresar el ID."""
        for i, estudiante in enumerate(estudiantes):
            if estudiante.id == id:
                estudiantes.pop(i)
                return {"status": "COMPLETED", "mensaje": "Estudiante eliminado"}
        return {"status": "ERROR", "mensaje": "Estudiante no encontrado"}

    # Método para modificar los datos de un estudiante existente
    @srpc(String(nillable=False), String(nillable=False), String(nillable=False), _returns=AnyDict)
    def modificarEstudiante(id, nuevo_nombre, nueva_carrera):  # noqa: A002
        """Modifica los datos de un estudiante existente en la lista mediante su ID."""
        for estudiante in estudiantes:
            if estudiante.id == id:
                estudiante.nombre = nuevo_nombre
                estudiante.carrera = nueva_carrera
                return {"status": "COMPLETED", "mensaje": "Estudiante actualizado"}
        return {"status": "ERROR", "mensaje": "Estudiante no encontrado"}


# Configuración de la aplicación SOAP
spyne_app = Application(
    services=[Estudiantes_Service],
    tns="com.dduenas.Estudiantes",
    name="Estudiantes",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)

