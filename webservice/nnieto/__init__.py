from . import etapa_01, etapa_02

wsgi_apps = {
    'alcancia/v1': etapa_01.wsgi_app,
    'alcancia/v2': etapa_02.wsgi_app,
}