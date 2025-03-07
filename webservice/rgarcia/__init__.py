from . import recipe_service

wsgi_apps = {
    'recetas/v1': recipe_service.wsgi_app,
}