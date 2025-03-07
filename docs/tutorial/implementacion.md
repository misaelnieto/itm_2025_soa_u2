# Paso 5 - Implementación de tu servicio web

## Introducción

La implementación de tu servicio web se hará usando varias tecnologías que ya están integradas en este repositorio. Pero para mayor referencia aquí tienes una lista de las más relevantes.

- `uv`: es el administrador de paquetes para administrar nuestro proyecto. La
  documentación se encuentra en
  [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/). Lo usamos para
  correr todos las herramientas de nuestro proyecto en un solo lado.
-  `python`: Es el lenguaje de programación que usaremos para escribir el
   servicio web y las pruebas.
- [WSGI](https://wsgi.readthedocs.io/en/latest/): Es un especificación de la
  comunidad Python que establece cómo se debe comunicar un servidor web con
  aplicaciones escritas en Python y cómo esas aplicaciones se pueden encadenar
  una tras otra para procesar una petición HTTP. Los servicios web SOAP son
  símplemente aplicaciones web que interactuan usando XML.
- [Spyne](http://spyne.io/): Spyne es una caja de herramientas para escribir aplicaciones SOAP y exponerlas como servicios web. Spyne permite múltiples protocolos y transportes. Nosotros usaremos únicamente el protocolo HTTP (WSGI) y el transporte SOAP 1.1.
- [Pytest](https://docs.pytest.org/en/stable/): Pytest es una librería de pruebas para Python que facilita la escritura de pruebas simples y escalables. Ofrece una sintaxis clara y concisa, soporte para fixtures, y una amplia gama de plugins para extender su funcionalidad. En nuestro proyecto usamos Pytest para realizar las pruebas de integración del servicio web.
- [Suds](https://fedorahosted.org/suds/): Suds es una librería de Python que facilita el consumo de servicios web SOAP. Permite generar clientes SOAP a partir de archivos WSDL, simplificando la interacción con servicios web mediante la creación automática de clases y métodos correspondientes a las operaciones definidas en el WSDL.
- Finalmente, usarás la herramienta [`webservice`](../herramientas/webservice.md) para hacer pruebas manuales de tu servicio web.

