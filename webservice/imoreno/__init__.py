from .HotelService import wsgi_app

wsgi_apps = {
	'HotelService/v1': wsgi_app,
}