from . import recetas

wsgi_apps = {
    'recetas': recetas.wsgi_app,
}