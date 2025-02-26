"""Fixtures para pruebas de servidores WSGI.

Este módulo proporciona fixtures de pytest y funciones de utilidad para probar servidores WSGI.
Funciones:
    _wait_for_tcp_port(host, port, timeout=2): Espera a que un puerto TCP esté disponible.
    _free_http_port(): Devuelve un puerto TCP libre proporcionado por el sistema operativo.
    wsgi_live_server(): Fixture de pytest que inicia un servidor WSGI en un puerto HTTP libre en un subproceso.
Fixtures:
    wsgi_live_server: Inicia un servidor WSGI en un puerto HTTP libre en un subproceso y devuelve la URL base del servidor.
"""

import logging
import socket
import threading

import pytest

from webservice.app import run_wsgi_server

logger = logging.getLogger(__name__)


def _wait_for_tcp_port(host, port, timeout=2):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # presumably
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except:  # noqa -- Any exception here means the port is not open anyway
        return False
    else:
        sock.close()
        return True


def _free_http_port():
    """Ask OS for a free TCP port we could use for our tests."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        addr = s.getsockname()
        return addr[1]


@pytest.fixture(scope='session')
def wsgi_live_server():
    """_Fixture_ que arranca el servidor WSGI en un hilo usando un puerto aleatorio.

    Este _fixture_ inicia un servidor WSGI en un puerto HTTP libre en un hilo.
    El servidor será terminado y limpiado después de que las pruebas hayan
    terminado.

    Yields:
        str: La URL base del servidor WSGI en ejecución.

    Ejemplo:
        def test_my_service(wsgi_live_server):
            base_url = wsgi_live_server
            response = requests.get(f"{base_url}/my-endpoint")
            assert response.status_code == 200
    """
    port = _free_http_port()
    if not isinstance(port, int) or not (0 < port < 65536):
        raise ValueError('Invalid port number')

    server_thread = threading.Thread(
        target=run_wsgi_server,
        kwargs={'host': '127.0.0.1', 'port': port, 'debug': False},
        daemon=True,
    )
    server_thread.start()

    logger.info('Waiting for the server to start')
    _wait_for_tcp_port('127.0.0.1', port)
    base_url = f'http://127.0.0.1:{port}'
    logger.info(f'Server started at {base_url}')

    return base_url
