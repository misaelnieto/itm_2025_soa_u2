"""Este módulo contiene el CRUD de nuestro webservice Peliculas.

Operaciones:

    - agregar pelicula:   Este servicio puede agregar una pelicula, si el cliente asi lo desea.
    - eliminar pelicula:  Este servicio se encarga de eliminar una pelicula segun el usuario lo necesite.
    - modificar pelicula: El servicio implemnta varios metodos que permiten modificar algun dato correspondiente de una pelicula, la razon por la que esta funcionalidad se implemento en varios metodos, fue para implementar una capa de restriccion, si obligamos al usario a que solo debe pasar los paramtros correspondientes a un dato para modificarlo, habra menos errores en la implementacion de dicho servicio.
    - obtener pelicula:   El usuario puede solicitar en su XML la informacion completa de una pelicula en particular, o de todas las peliculas.

En esta etapa, las operaciones se realizan sobre una lista en memoria.
En una implementacion real, se recomienda utilizar una base de datos para persistencia.
"""

from spyne import Application, ComplexModel, Integer, Service, String, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Movie(ComplexModel):
    """Modelo de datos que representa una pelicula en una plataforma de streaming."""
    name = String
    release = Integer
    director = String


    
class MoviesServices(Service):
    """Servicio con el cual, podemos tener las operaciones mencionadas al inicio."""

    Movies = []

    @srpc(String,Integer,String,_returns=String)
    def addMovie(name,release,director):
        """Este metodo de python permite agregar una pelicula a la lista de la clase."""
        # Crear la instancia
        movie = Movie(name=name,release=release,director=director)
        MoviesServices.Movies.append(movie)

        return "Pelicula agrega correctamente"


    @srpc(String,_returns=Movie)
    def getMovie(name):
        """Este metodo de python itera sobre el arreglo de clase que tenemos, una vez que encuentre una pelicula con el nombre que el usuario le pase como argumento, nos va a devolver toda la pelicula, es decir, el objeto Movie que contiene todos los datos de dicha pelicula."""
        for movie in MoviesServices.Movies:
           if movie.name == name:
               return movie
           
        return None


    @srpc(String,_returns=String)
    def deleteMovie(name):
        """Este metodo itera sobre la lista, una vez que encuentra la pelicula a la que el cliente hace referencia, la elimina, de lo contrario, retorna un mensaje, el cual estara dentro de un XML que se enviara como respuesta al cliente, avisandole que la pelicula que el cliente intento eliminar no existe."""
        deleted = 0

        for movie in MoviesServices.Movies:
           if movie.name == name:
               MoviesServices.Movies.remove(movie)
               deleted = 1
           
        if deleted == 0:
            return f"No existe la pelicula {name}, por lo que no se hizo ninguna eliminacion"
        
        return "La pelicula se elimino con exito"

    
    @srpc(String, String, _returns=String)
    def changeName(old_name,new_name):
        """Metodo de python para cambiar el nombre, itera sobre todas las peliculas, encuentra la pelicula en cuestion, y cambia el nombre anterior por uno nuevo."""
        for movie in MoviesServices.Movies:
           if movie.name == old_name:
               movie.name = new_name
               return f"El nombre de la pelicula {old_name} fue modificado a {new_name}"
        
        return "No existe la pelicula que quieres modificar"


    @srpc(String, Integer, _returns=String)
    def changeRelease(name,new_release):
        """Similar al metodo anterior, solo que este modifica la fecha de lanzamiento de la pelicula en cuestion."""
        for movie in MoviesServices.Movies:
           if movie.name == name:
               movie.release = new_release
               return f"El año de lanzamiento de la pelicula {name} fue modificado a {new_release}"
        
        return "No existe la pelicula que quieres modificar"

    @srpc(String, String, _returns=String)
    def changeDirector(name,new_director):
        """Similar al metodo anterior, solo que este modifica el nombre del director de la pelicula en cuestion."""
        for movie in MoviesServices.Movies:
           if movie.name == name:
               movie.director = new_director
               return f"El director de la pelicula {name} fue modificado a {new_director}"
        
        return "No existe la pelicula que quieres modificar"




# Todo lo de abajo es para que el servicio pueda ejecutar en un servidor web  # noqa: FIX002

# spyne es el que genera automaticamente los mensajes XML

# La configuracion debe de ir en una variable spyne_app
spyne_app = Application(
    services=[MoviesServices],
    tns='com.ksoto.movies',   # <-- todos los XML que vamos a recibir, van a tener el name space: com.ksoto.movies                                          
    name='Movies',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(validator='lxml'),
)


wsgi_app = WsgiApplication(spyne_app)