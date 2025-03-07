"""Este es una aplicación WSGI que responde con un mensaje de texto plano.

Ver https://werkzeug.palletsprojects.com/en/stable/tutorial/ para más información.
"""

from werkzeug.wrappers import Response


def application(environ, start_response):
    """Función WSGI que responde con un mensaje de texto plano."""
    response = Response("Hola. Este es un servicio web SOAP. !", mimetype='text/plain')
    return response(environ, start_response)
