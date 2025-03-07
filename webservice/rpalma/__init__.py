from . import contactos

wsgi_apps = {
    'contactos': contactos.wsgi_app,
}