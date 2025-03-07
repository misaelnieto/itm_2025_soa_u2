# Pruebas de integración con `pytest`

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

