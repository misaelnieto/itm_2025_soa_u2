import pytest  # noqa: D100
from suds.client import Client as SoapClient


@pytest.fixture
def ws(wsgi_live_server):
    """Fixture que inicializa un cliente SOAP para el servidor WSGI."""
    base_url = wsgi_live_server
    service_url = f'{base_url}/ws/ksoto/peliculas'
    wsdl_url = f'{service_url}?wsdl'
    return SoapClient(wsdl_url)



def test_wsdl_metadata(ws):
    """Test that our server provides valid WSDL metadata."""
    # First check the target namespace is correct. This will fail when you change the tns in the webservice.py
    assert ws.wsdl.tns == ('tns', 'com.ksoto.movies')

    # Inspect the service definition
    sd = ws.sd[0]
    assert sd.service.name == 'MoviesServices'
    # We have one port, named Alcancia, that points to the root of the service ...
    assert len(sd.service.ports) == 1
    svc_port = sd.service.ports[0]
    assert svc_port.name == 'Movies'

    # Has 7 methods and 16 types
    assert len(svc_port.methods) == 6
    assert len(sd.types) == 13



def test_service_methods(ws):
    """Este metodo de python contiene las pruebas requeridas."""
    # Agregar titanic
    ws.service.addMovie('Titanic',1997,'James Cameron')  


    # Comprobar si funciona el metodo getMovie
    response = ws.service.getMovie('Titanic')
    assert response.release == 1997    


    # Comprobar si cuando buscamos una pelicula que no existe, efectivamente nos retorna None
    response = ws.service.getMovie('Seitokai Yakuindomo')
    assert response is None   
    


    # Agregar otra pelicula
    response = ws.service.addMovie('A new hope',1977,'George Lucas')
    assert response == "Pelicula agrega correctamente"  # < -- Comprobar que nos retorno la respuesta de exito
    



    # Vamos a agregar una pelicula con datos erroneos
    ws.service.addMovie('The shawshank redemption',1990,'Tobey Maguire')  
    response = ws.service.changeRelease("The shawshank redemption",1994)
    assert response == "El año de lanzamiento de la pelicula The shawshank redemption fue modificado a 1994"
    response = ws.service.changeDirector("The shawshank redemption","Frank Darabont")
    assert response == "El director de la pelicula The shawshank redemption fue modificado a Frank Darabont"
    # Intentar cambiar el nombre de una pelicula que no existe
    response = ws.service.changeName("Me gusta la gasolina","nuevo nombre XDXDXD")
    assert response == "No existe la pelicula que quieres modificar"



    # Eliminar una pelicula
    response = ws.service.deleteMovie("The shawshank redemption")
    assert response == "La pelicula se elimino con exito"



    # Vamos a eliminar una pelicula que no existe
    response = ws.service.deleteMovie('Onichan')
    assert response == "No existe la pelicula Onichan, por lo que no se hizo ninguna eliminacion"


    # Vamos a cambiar el nombre de la pelicula:  The shawshank redemption
    response = ws.service.changeName('A new hope','One Piece')
    assert response == "El nombre de la pelicula A new hope fue modificado a One Piece"


    # Vamos a cambiar la fecha de lanzamiento de una pelicula que no existe
    response = ws.service.changeRelease('Me gusta Itsuki Nakano',2019)
    assert response == "No existe la pelicula que quieres modificar"


    # Vamos a cambiar el director de una pelicula que no existe
    response = ws.service.changeDirector('Pelicula Nueva','otro director')
    assert response == "No existe la pelicula que quieres modificar"
    


# corremos --->    uv run pytest
# Tenemos que ejecutar el comando en ksoto