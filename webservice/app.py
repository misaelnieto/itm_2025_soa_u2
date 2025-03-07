"""Módulo principal del servicio web.

Este módulo contiene la función principal para iniciar un servidor WSGI para que
puedas desarrollar tu servicio web de manera interactiva. 

La función principal es `start_server()` que se encarga de iniciar un servidor
WSGI en el puerto y host especificado. 

La función `_find_wsgi_apps()` se encarga de buscar todos los módulos dentro del
paquete `webservice` que tengan un atributo `wsgi_app` o `wsgi_apps`. Cuando
encuentra alguno de estos atributos, lo instala en el servidor WSGI en la ruta
`/ws/<nombre_del_modulo>` o `/ws/<nombre_del_modulo>/<nombre_del_app>`
respectivamente.

### Usand `wsgi_app`

Si tu módulo se llama `webservice/ffernandez` y tiene un objeto llamado
`wsgi_app` entonces tu aplicación estará disponible en
`http://localhost:8080/ws/ffernandez`. Si ese objeto es además un servicio web
de spyne, encontrarás el wsdl en `http://localhost:8080/ws/ffernandez?wsdl`.

### Usando `wsgi_apps`

Si tu módulo se llama `webservice/ffernandez` y tiene un diccionario llamado
`wsgi_apps` entonces se usarán las llaves de ese diccionario como rutas y los
valores como aplicaciones WSGI. Por ejemplo, si tienes un diccionario así:

```python wsgi_apps = {
    'app1': app1, 'app2': app2
}
```

Entonces se publicarán dos aplicaciones en las rutas `/ws/ffernandez/app1` y
`/ws/ffernandez/app2` respectivamente.

### Usando `wsgi_app` y `wsgi_apps` juntas

Si tu módulo tiene ambos objetos, se se usará `wsgi_app` y `wsgi_apps` será
ignorado.

### Cuando ninguno de los dos está presente

Si tu módulo no tiene ninguno de los dos objetos, entonces solo se mostrará un
mensaje de advertencia en los logs y el módulo será ignorado.

### Uso de start_server()

El comando `start_server()` está disponible desde la línea de comandos con el
nombre `webservice`. Lo puedes usar para iniciar el servidor WSGI. Puedes usarlo
en una consola de windows para iniciar el servidor. La forma de usarlo es la
siguiente:

```shell uv run webservice ```

"""
import importlib
import logging
import pkgutil

import click
from colorlog import ColoredFormatter
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from webservice.frontend import application as frontend_app

logger = logging.getLogger(__name__)


def _find_wsgi_apps():
    package = importlib.import_module('webservice')
    wsgi_apps = {}
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if not is_pkg:
            continue
        ws_module = importlib.import_module(f'webservice.{module_name}')
        if hasattr(ws_module, 'wsgi_app'):
            app_path = f'/ws/{module_name}'
            wsgi_apps[app_path] = ws_module.wsgi_app
            logger.info(f'Instalando app WSGI en {app_path}')
        elif hasattr(ws_module, 'wsgi_apps'):
            for pth, app in ws_module.wsgi_apps.items():
                app_path = f'/ws/{module_name}/{pth}'
                wsgi_apps[app_path] = app
                logger.info(f'Instalando app WSGI en {app_path}')
        else:
            logger.warning(f'El módulo {module_name} no tiene un objeto wsgi_app o wsgi_apps. Ignorando...')
    return wsgi_apps



def run_wsgi_server(host, port, debug):
    """Inicia un servidor WSGI en el host y puerto especificado.
    
    Parámetros:
        host -- El host donde se va a iniciar el servidor.
        port -- El puerto donde se va a iniciar el servidor.
        debug -- Activa el modo de depuración.
    """
    app = DispatcherMiddleware(frontend_app, _find_wsgi_apps())
    run_simple(host, port, app, use_debugger=debug, use_reloader=debug)



@click.command()
@click.option('--host', '-h', default='127.0.0.1', help='Puerto HTTP', show_default=True)
@click.option('--port', '-p', default=8080, type=int, help='Puerto HTTP', show_default=True)
@click.option('--debug', '-d', is_flag=True, help='Activa el modo de depuración')
def main(host, port, debug):  # pragma: no cover
    """Inicia un servidor WSGI en el host y puerto especificado."""
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    run_wsgi_server(host, port, debug)
