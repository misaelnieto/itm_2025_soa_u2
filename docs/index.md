# Arquitectura Orientada a Servicios

Instituto Tecnológico de Mexicali - 2005-1


## Unidad 2 - Servicios Web SOAP

El objetivo de esta unidad es hacer que obtengas experiencia practica implementando y consumiendo un servicio web SOAP.

En este repositorio integrarás tu trabajo en forma de un pull request (PR) de github.
Para que el PR sea integrado en la rama principal (main), debe de cumplir los siguientes requisitos:

- [x] El módulo del estudiante contiene un archivo `README.md`
- [x] El archivo `README.md` contiene la descripción de tu servicio y los requerimientos funcionales.
- [x] El archivo `README.md` describe en qué ruta se accede a tu servicio web
- [x] El archivo `README.md` describe las operaciones y tipos de datos que tu servicio web exporta.
- [x] Se han implementado todos los requerimientos funcionales
- [x] Incluye pruebas integración
- [x] Todas las pruebas pasan
- [x] El análisis de cobertura de código es de 100%
- [x] Todos los errores del análisis estático de código han sido arreglados.

!!! warning "Fecha límite para enviar sus PR"
    Todos los PRs deberán ser debidamente integrados a la rama principal** a más tardar a las 5pm (Hora del pacífico) del Viernes 7 de Marzo**.




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

!!! info "Manos a la obra"
    Buena suerte

