En esta sección encontrarás información técnica necesaria para echar a andar tu servicio web.


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



## Referencia de la herramienta de línea de comandos `webservice`


::: mkdocs-click
    :module: webservice.app
    :command: main
