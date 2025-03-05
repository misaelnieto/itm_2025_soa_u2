from spyne import Service, ComplexModel, String, Integer, srpc, Application, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Movie(ComplexModel):
    name = String
    release = Integer
    director = String



class MoviesServices(Service):

    Movies = []

    @srpc(String,Integer,String,_returns=String)
    def addMovie(name,release,director):

        # Crear la instancia
        movie = Movie(name=name,release=release,director=director)
        MoviesServices.Movies.append(movie)

        return "Pelicula agrega correctamente"


    @srpc(String,_returns=Movie)
    def getMovie(name):
        
        for movie in MoviesServices.Movies:
           if movie.name == name:
               return movie
           
        return None
    

    @srpc(_returns=Array(Movie))
    def getMovies():
        return MoviesServices.Movies


    @srpc(String,_returns=String)
    def deleteMovie(name):

        deleted = 0

        for movie in MoviesServices.Movies:
           if movie.name == name:
               MoviesServices.Movies.remove(movie)
               deleted = 1
           
        if deleted == 0:
            return "No se hay un la pelicula"
        else:
            return "La pelicula se elimino con exito"


    @srpc(String,_returns=String)
    def updateMovie(name):

        for movie in MoviesServices.Movies:
           if movie.name == name:
               movie.release = 2019
               return "Datos modificados exitosamente"
        
        return "No se encontro la pelicula que quieres modificar"




# Todo lo de abajo es para que el servicio pueda ejecutar en un servidor web

# spyne es el que genera automaticamente los mensajes XML

# La configuracion debe de ir en una variable spyne_app
spyne_app = Application(
    services=[MoviesServices],
    tns='com.ksoto.movies',   # <-- todos los XML que vamos a recibir, van a tener el name space: com.ksoto.movies                                          
    name='Movies',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(validator='lxml')
)


wsgi_app = WsgiApplication(spyne_app)