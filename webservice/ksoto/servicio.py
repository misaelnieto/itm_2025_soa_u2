from spyne import Service, ComplexModel, Unicode, Integer, srpc


class Movie(ComplexModel):
    name = Unicode
    release = Integer
    director = Unicode



class PeliculasServices(Service):

    Movies = []

    @srpc(Unicode,Integer,Unicode,_returns=Unicode)
    def addMovie(name,release,director):

        # Crear la instancia
        movie = Movie(name=name,release=release,director=director)
        PeliculasServices.Movies.append(movie)

        return "Pelicula agrega correctamente"


    @srpc(Unicode,_returns=Movie)
    def getMovie(name):
        
        for movie in PeliculasServices.Movies:
           if movie.name == name:
               return movie
           
        return None


    @srpc(Unicode,_returns=Unicode)
    def deleteMovie(name):

        deleted = 0

        for movie in PeliculasServices.Movies:
           if movie.name == name:
               PeliculasServices.Movies.remove(movie)
               deleted = 1
           
        if deleted == 0:
            return "No se hay un la pelicula"
        else:
            return "La pelicula se elimino con exito"


    @srpc(Unicode,_returns=Unicode)
    def updateMovie(name):

        for movie in PeliculasServices.Movies:
           if movie.name == name:
               movie.release = 2019
               return "Datos modificados exitosamente"
        
        return "No se encontro la pelicula que quieres modificar"