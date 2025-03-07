"""Pruebas relacionadas con el frontend de la aplicación."""

from werkzeug.test import Client

from webservice.frontend import application as frontend_app


def test_frontend():
    """Test the frontend application."""
    client = Client(frontend_app, use_cookies=True)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Hola. Este es un servicio web SOAP' in response.text
