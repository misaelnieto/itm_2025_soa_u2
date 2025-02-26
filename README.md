# Arquitectura Orientada a Servicios

## Unidad 2 - Servicios Web SOAP

El objetivo de esta unidad es hacer que el estudiante obtenga experiencia practica implementando un servicio web con SOAP y que posteriormente lo consuma.

En este repositorio el estudiante integrará su trabajo en forma de un pull request (PR) de github.
Para que el PR sea integrado en la rama principal (main), debe de cumplir los siguientes requisitos:

- [x] El módulo del estudiante contiene un archivo `README.md`
- [x] El archivo `README.md` contiene la descripción de su servicio y los requerimientos funcionales.
- [x] El archivo `README.md` describe en qué ruta se accede a su servicio web
- [x] El archivo `README.md` describe las operaciones y tipos de datos que su servicio web exporta.
- [x] Se han implementado todos los requerimientos funcionales
- [x] Incluye pruebas integración
- [x] Todas las pruebas pasan
- [x] El análisis de cobertura de código es de 100%
- [x] Todos los errores del análisis estático de código han sido arreglados.

> :warning: Todos los PRs deberán ser debidamente integrados a la rama principal** a más tardar a las 5pm (Hora del pacífico) del Viernes 7 de Marzo**.


### Asignación de nombre de módulos

| Estudiante | Nombre de módulo | Módulo de servicio web | Módulo de pruebas |
| --- | --- | --- | --- |
| Juan Carlos Paredes Gatopo | `jparedes` | `webservice.jparedes` | `tests.jparedes` |
| Diego Iván Dueñas Padilla | `dduenas` | `webservice.dduenas` | `tests.dduenas` |
| David Ramos Luna | `dramos` | `webservice.dramos` | `tests.dramos` |
| Rodolfo García Galaz | `rgarcia` | `webservice.rgarcia` | `tests.rgarcia` |
| Karim Antonio Soto López | `ksoto` | `webservice.ksoto` | `tests.ksoto` |
| Rosa Elena Palma y Meza Buelna | `rpalma` | `webservice.rpalma` | `tests.rpalma` |
| Kevin Hernandez Zazueta | `khernandez` | `webservice.khernandez` | `tests.khernandez` |
| Jazmin Heredia Cota | `jheredia` | `webservice.jheredia` | `tests.jheredia` |
| José Manuel Arce Higuera | `jarce` | `webservice.jarce` | `tests.jarce` |
| Isaí Moreno Mendoza | `imoreno` | `webservice.imoreno` | `tests.imoreno` |
| Imanol Maximiliano Mayo Alvaro | `imayo` | `webservice.imayo` | `tests.imayo` |
| Jesús Javier Chaidez Delgado | `jchaidez` | `webservice.jchaidez` | `tests.jchaidez` |
| Javier Contreras Partida | `jcontreras` | `webservice.jcontreras` | `tests.jcontreras` |
| Adrian Fernando Santelis Mendoza | `asantelis` | `webservice.asantelis` | `tests.asantelis` |
| Fabian Ignacio Calzada Lozano | `fcalzada` | `webservice.fcalzada` | `tests.fcalzada` |


### Procedimiento para crear tus prácticas


1. Revisa tu módulo de servicio web y módulo de pruebas asignado
2. Haz un Fork de este repositorio en tu cuenta personal de Github
3. Implementa tu servicio web en tu módulo de servicio web asignado.
   > :point_right: No olvides exponer un objeto llamado `wsgi_app` en tu módulo de servicio web para el middleware de WSGI publique tu aplicación automáticamente. Por ejemplo, si tu nombre de módulo es `ffernandez`, el middleware de WSGI buscará la aplicación WSGI en `webservice.ffernandez.wsgi_app`. Si la encuentra, la publicará en la ruta `/ws/ffernadez`. Si no la encuentra, el servidor web sólo registrará una advertencia. 
4. Escribe las pruebas de integración en en tu módulo de pruebas asignado.
5. Documenta tu servicio web en el archivo `README.md` dentro de tu módulo de servicio web.

## Configuración de tu entorno de trabajo

### Editor de código

Puedes usar el editor de código de tu preferencia. El profesor usa Visual Studio Code y ha pre-configurado el entorno para que te sea más fácil desarrollar tu trabajo.

### Instalación de python, `uv` y entorno virtual

Sigue el proceso de instalación de `uv` desde la página oficial https://docs.astral.sh/uv/.

Una vez que hayas instalado y configurado `uv`, cincroniza las dependencias y versión de python con el siguiente comando:

```shell
uv sync
```

La primera vez que corras este comando, `uv` descargará la versión de Python adecuada, creara un entorno virtual e instalará todas las dependencias necesarias para tus prácticas.

### Arrancando el servidor web de desarrollo

```
uv run webservice
```

Cuando hagas cambios en tu código, el servidor reiniciará automáticamente. Recuerda revisar los errores y advertencias en la terminal donde estas ejecutando el servidor. Presiona `Ctrl`+`C` para terminar la ejecución del servidor de pruebas.

### Corriendo las pruebas con pytest

El siguiente comando correrá todas las pruebas contenidas en el módulo `tests`

```
uv run pytest
```

Si solo deseas correr las pruebas las pruebas contenidas en tu módulo asignado de pruebas, simplemente proporciona la ruta al módulo que contiene la prueba que deseas correr. Por ejemplo, si tu prueba esta en `tests/test_ffernandez.py`, el comando de `pytest` sería:


```
uv run pytest tests/test_ffernandez.py
```

También es posible correr una sola prueba dentro de un módulo de la siguiente manera:


```
uv run pytest tests/test_ffernandez.py::test_abc
```

Consulta la documentación de `pytest` en https://docs.pytest.org/en/stable/ para obtener más información acerca de su uso y sus diferentes maneras de invocar y depurar pruebas.


### Corriendo el analizador de código estático

WIP

```
uv run ruff check .
```


