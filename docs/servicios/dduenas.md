# Proyecto Estudiantes

## Módulo `estudiantes`

::: webservice.dduenas.servicio

Estructura del Código

1. Modelo de Datos: Estudiante

class Estudiante(ComplexModel):
    nombre = String
    id = String
    carrera = String

La clase Estudiante extiende ComplexModel de Spyne para definir las propiedades de un estudiante.

class Estudiante(ComplexModel):
    nombre = String
    id = String
    carrera = String

2. Lista Inicial de Estudiantes

Se define una lista predefinida con dos estudiantes de ejemplo.

estudiantes = [
    Estudiante(nombre="David", id="21490540", carrera="Sistemas"),
    Estudiante(nombre="Juan", id="21490539", carrera="Sistemas"),
]

3. Servicio: Estudiantes_Service

Esta clase contiene los métodos expuestos a través del servicio SOAP.

listado()

Devuelve un array con todos los estudiantes registrados.

@srpc(_returns=Array(Estudiante))

altaEstudiante(id, nombre, carrera)

Agrega un nuevo estudiante a la lista.

@srpc(String, String, String, _returns=AnyDict)

eliminarEstudiante(id)

Elimina un estudiante basado en su ID.

@srpc(String(nillable=False), _returns=AnyDict)

modificarEstudiante(id, nuevo_nombre, nueva_carrera)

Permite actualizar la información de un estudiante existente.

@srpc(String, String, String, _returns=AnyDict)

4. Configuración de la Aplicación

Se configura la aplicación Spyne con el protocolo SOAP 1.1 y se prepara para ser ejecutada como una aplicación WSGI.

spyne_app = Application(
    services=[Estudiantes_Service],
    tns="com.dduenas.Estudiantes",
    name="Estudiantes",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)

Ejecución

Puedes utilizar cualquier servidor WSGI como gunicorn o el servidor integrado de wsgiref para ejecutar la aplicación.