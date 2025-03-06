Lo que se hizo en este proyecto fue crear un servicio de peliculas, en donde una persona puede manejar informacion relacionada con peliculas, como agregar peliculas a un catalogo, eliminar peliculas de un catalogo, modificar data relacionada con alguna pelicula en cuestion entre otras cosas. Sin mas que explicar, expliquemos el codigo:

Tenemos el archivo webservice/ksoto/servicio.py, en este archivo tenemos el servicio en si, toda la logica de lo que hara nuestro servicio se encuentra en este archivo. Voy a explicar paso a paso que hace cada cosa:







Aqui solo estamos haciendo las importaciones que vamos a utlizar en nuestro codigo, como podemos ver, todo viene de la libreria spyne.

    from spyne import Service, ComplexModel, String, Integer, srpc, Application, Array
    from spyne.protocol.soap import Soap11
    from spyne.server.wsgi import WsgiApplication




Esta es la clase Movie, basicamente es por decirlo un nodo, en donde guardaremos la informacion correspondiente de cada pelicula, en spyne, necesitamos definir el tipo de dato que es cada variable, algo que en python no es normal, pero que en otros lenguajes de programacion si lo es.

        class Movie(ComplexModel):
            name = String
            release = Integer
            director = String




Luego tenemos la clase principal, en esta clase es donde vamos a manejar toda la logica de nuestro servicio, dentro de esta clase tenemos todas las funciones mencionadas al principio de la documentacion. Podemos notar que la clase recibe como argumento Service, esto es significa que es un servicio de SOAP. Tambien podemos notar que tenemos un arreglo, dentro de este arreglo, vamos a almacenar las peliculas.

    class MoviesServices(Service):

        Movies = []





Cuando trabajamos con spyne, todas las funciones deben tener un decorador, en ellos, debemos de poner los tipos de datos que recibe, es decir, el tipo de dato de cada argumento que recibe, como el tipo de dato que retorna. En este caso, la variable name se espera que sea de tipo string, la variable release, se espera que se de tipo Integer. Como podemos ver en la funcion, al final nos retorna un mensaje de exito, es decir, un string, por lo que en el decorador debemos especificar que tipo de dato retorna, es decir, un string.

El metodo addMovie recibe toda la DATA relacionada con una pelicula, a partir de esa DATA, crea una instancia, y dicha instancia la agrega a la lista Movies. Por ultimo retorna un mensaje de exito

        @srpc(String,Integer,String,_returns=String)
        def addMovie(name,release,director):

            # Crear la instancia
            movie = Movie(name=name,release=release,director=director)
            MoviesServices.Movies.append(movie)

            return "Pelicula agrega correctamente"





Este metodo lo unico que hace es recibir un nombre, entonces a traves de un for, busca en la lista alguna pelicula que concorde con el nombre, si no encuentra ninguna coincidencia, entonces significa que la pelicula que esta buscando el usuario no existe, si encuentra una coincidencia, entonces retorna toda la pelicula, es decir, un dato de tipo Movie.

        @srpc(String,_returns=Movie)
        def getMovie(name):
                
            for movie in MoviesServices.Movies:
                if movie.name == name:
                    return movie
                
            return None




Este metodo solo retorna la lista completa de todas las peliculas.

        @srpc(_returns=Array(Movie))
        def getMovies():
            return MoviesServices.Movies





Este metodo lo que hace es que pide un nombre, busca una coincidencia, es decir, una pelicula que tenga el mismo nombre, si la encuentra, entonces procede a eliminar la pelicula en si, es decir, no borra simplemente el nombre, la fecha en la que salio, el nombre del director, sino toda la pelicula en si, por lo que en la lista, ya no aparece mas dicha pelicula. Utiliza un bucle for para iterar sobre la lista, ademas de que se usa una variable para verificar si la eliminacion fue exitosa o no.

        @srpc(String,_returns=String)
        def deleteMovie(name):

            deleted = 0

            for movie in MoviesServices.Movies:
            if movie.name == name:
                MoviesServices.Movies.remove(movie)
                deleted = 1
            
            if deleted == 0:
                return f"No existe la pelicula {name}, por lo que no se hizo ninguna eliminacion"
            else:
                return "La pelicula se elimino con exito"





Este metodo, al igual que el metodo de eliminacion, utiliza un ciclo for para iterar sobra cada pelicula, si encuentra la pelicula que el cliente (otro programa) quiere, entonces procede a cambiar el nombre, ya que este metodo solo modifica el nombre, es decir, si una pelicula se llamaba mi pobre angelito, ahora esa pelicula se puede llamar Seitokai Yakuindomo

        @srpc(String, String, _returns=String)
        def changeName(old_name,new_name):
            for movie in MoviesServices.Movies:
            if movie.name == old_name:
                movie.name = new_name
                return f"El nombre de la pelicula {old_name} fue modificado a {new_name}"
            
            return "No existe la pelicula que quieres modificar"





Este metodo hace lo mismo que changeName, solo que este cambie la fecha de lanzamiento de dicha pelicula, pero es la fecha de lanzamiento en Estados Unidos. Bueno eso tambien dependera del cliente.

        @srpc(String, Integer, _returns=String)
        def changeRelease(name,new_release):
            for movie in MoviesServices.Movies:
            if movie.name == name:
                movie.release = new_release
                return f"El año de lanzamiento de la pelicula {name} fue modificado a {new_release}"
            
            return "No existe la pelicula que quieres modificar"






Este metodo hace lo mismo que los otros dos metodos anteriores, solo que este cambie el nombre del director de una pelicula, esto es debido a que en ocasiones, uno puede equivocarse con respecto al nombre del director, por ejemplo, yo pensaba que la pelicula "THE EMPIRE STRIKES BACK", la segunda pelicula de STAR WARS, fue dirigida por George Lucas, y aunque el encargado de la pelicula si fue George Lucas, el papel de director fue otra persona.

        @srpc(String, String, _returns=String)
        def changeDirector(name,new_director):
            for movie in MoviesServices.Movies:
            if movie.name == name:
                movie.director = new_director
                return f"El director de la pelicula {name} fue modificado a {new_director}"
            
            return "No existe la pelicula que quieres modificar"





Por ultimo, tenemos que crear la configuracion de spyne, es decir, para la comunicacion con el cliente-servidor, spyne nos dice que dicha documentacion la tenemos que guardar en una variable spyne_app, dentro, tenemos que poner que servicios queremos, en este caso, tenemos que poner el servicio (El nombre de la clase que creamos) que queremos, el tns, que en mi caso, le puse 'com.ksoto.movies'. Basicamente esto no afecta en tal a la logica de nuestro servicio, es la pura configuracion, pero si no ponemos esto, de nada nos servira que tengamos el mejor servicio del planeta tierra, si nadie se puede conectarse a ella.

spyne_app = Application(
    services=[MoviesServices],
    tns='com.ksoto.movies',   # <-- todos los XML que vamos a recibir, van a tener el name space: com.ksoto.movies                                          
    name='Movies',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(validator='lxml')
)


wsgi_app = WsgiApplication(spyne_app)






 -------------------------------------------------------------------------------------





Ahora explicare lo que tenemos en el archivo _init_.py


        from .servicio import wsgi_app

        wsgi_apps = {
            'ksoto/movies': wsgi_app,
        }


En python, un archivo llamado _init_.py dentro de un directorio indica que dicho directorio debe tratarse como un paquete. En este proyecto, _init_.py tiene la funcion principal de organizar y exponer el servicio WSGI desarrollado por Spyne.
