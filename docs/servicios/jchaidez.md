# Servicio Web SOAP - Gestión de Cursos

Este servicio web permite gestionar cursos mediante operaciones CRUD (Crear, Leer, Actualizar, Eliminar). Está desarrollado en Python utilizando **Spyne** para la creación del servicio SOAP, y expuesto a través de **WSGI** para su integración con un servidor web. Este servicio está diseñado para manipular una lista de cursos en memoria, ideal para pruebas, aunque se recomienda una base de datos en una implementación real.

## Requisitos Funcionales

El servicio web ofrece las siguientes funcionalidades:

- **Listar todos los cursos existentes**.
- **Buscar un curso por su nombre o ID**.
- **Agregar un nuevo curso**.
- **Eliminar un curso por su nombre o ID**.
- **Actualizar los datos de un curso existente**.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación.
- **Spyne**: Framework para la creación de servicios web SOAP.
- **WSGI**: Interfaz para desplegar el servicio en servidores web.
- **Suds**: Cliente SOAP para realizar pruebas.
- **Pytest**: Framework de pruebas.
- **lxml**: Biblioteca para la validación del XML.

## Ruta de Acceso al Servicio Web

El servicio está disponible en la siguiente ruta de acceso:
/ws/jchaidez

La dirección completa dependerá de la configuración del servidor WSGI.

## Operaciones Disponibles

A continuación se describen las operaciones que el servicio web expone, junto con sus parámetros y tipos de retorno:

### 1. `listado_cursos`

- **Descripción**: Devuelve la lista de todos los cursos existentes en el sistema.
- **Parámetros**: Ninguno.
- **Retorno**: Un arreglo de objetos `Curso` con los siguientes campos:
  - `id_curso`: Identificador único del curso.
  - `nombre`: Nombre del curso.
  - `profesor`: Profesor asignado al curso.

### 2. `buscar_curso(nombre: str, id_curso: int)`

- **Descripción**: Busca un curso por nombre o ID. Retorna los detalles del curso si se encuentra, o un mensaje de error si no se encuentra.
- **Parámetros**:
  - `nombre` (opcional): Nombre del curso.
  - `id_curso` (opcional): Identificador único del curso.
- **Retorno**: Un diccionario con los siguientes campos:
  - `status`: "OK" si se encuentra el curso, "ERROR" si no.
  - `id_curso`: Identificador único del curso.
  - `nombre`: Nombre del curso.
  - `profesor`: Nombre del profesor.
  - `mensaje`: Mensaje adicional en caso de error (si no se encuentra el curso).

### 3. `agregar_curso(id_curso: int, nombre: str, profesor: str)`

- **Descripción**: Agrega un nuevo curso a la lista.
- **Parámetros**:
  - `id_curso`: Identificador único del curso.
  - `nombre`: Nombre del curso.
  - `profesor`: Nombre del profesor asignado al curso.
- **Retorno**: Un diccionario con los siguientes campos:
  - `status`: "OK" si el curso se agrega correctamente, "ERROR" si el ID ya existe.
  - `id_curso`: Identificador del curso agregado.
  - `nombre`: Nombre del curso agregado.
  - `profesor`: Profesor asignado al curso agregado.

### 4. `eliminar_curso(nombre: str, id_curso: int)`

- **Descripción**: Elimina un curso de la lista por su nombre o ID.
- **Parámetros**:
  - `nombre`: Nombre del curso.
  - `id_curso`: Identificador único del curso.
- **Retorno**: Un diccionario con los siguientes campos:
  - `status`: "OK" si el curso se elimina correctamente, "ERROR" si no se encuentra el curso.
  - `mensaje`: Mensaje adicional sobre el resultado de la operación.

### 5. `actualizar_curso(id_curso: int, nuevo_nombre: str, nuevo_profesor: str)`

- **Descripción**: Actualiza los datos de un curso existente mediante su ID.
- **Parámetros**:
  - `id_curso`: Identificador único del curso.
  - `nuevo_nombre`: Nuevo nombre del curso.
  - `nuevo_profesor`: Nuevo nombre del profesor asignado.
- **Retorno**: Un diccionario con los siguientes campos:
  - `status`: "OK" si el curso se actualiza correctamente, "ERROR" si no se encuentra el curso.
  - `mensaje`: Mensaje adicional sobre el resultado de la operación.

## Pruebas de Integración

Las pruebas de integración para el servicio web están ubicadas en el módulo `tests/jchaidez`, y pueden ejecutarse con el siguiente comando:
uv run pytest tests/jchaidez

## Cobertura de Código

Para ejecutar el análisis de cobertura de código y verificar la calidad del mismo, utiliza:
uv run pytest --cov=webservice.jchaidez

## Análisis Estático de Código

Para verificar errores de estilo y calidad de código, utiliza la herramienta `ruff` con el siguiente comando:
uv run ruff check .

## Notas

- Actualmente, los cursos se almacenan en una lista en memoria para simplificar el desarrollo y las pruebas.
- En un entorno real, se recomienda utilizar una base de datos para persistencia.
- El servicio está diseñado con las mejores prácticas de desarrollo usando **Spyne** y **WSGI**.

## Documentación generada automáticamente

::: webservice.jchaidez
