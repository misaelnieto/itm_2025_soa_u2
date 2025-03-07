from . import HotelService

wsgi_apps = {
    'HotelService/v1': HotelService.wsgi_app,
}