"""Este modulo contiene el proyecto de Recetas.

Operaciones:
    -`recetas`: Devuelve todas las recetas almacenadas.
    -`ver_receta`: Devuelve una receta en particular.
    -`buscar_por_ingrediente`: Devuelve las recetas que contenga un ingrediente dado.
    -`registrar`: Agrega una receta en el catálogo de recetas.
    -`actualizar: Actualiza una receta si existe en el catálogo de recetas.
    -`borrar`: Borra una receta del catálogo de recetas.
"""
from spyne import Application, Array, ComplexModel, Service, String, Unicode, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Receta(ComplexModel):
    """Modelo que representa una receta.
    
    Incluye un listado de ingrediente y un listado de pasos.
    """

    nombre = String
    descripcion = String
    ingredientes = Array(String)
    pasos = Array(String)

_recetas_db = [
        Receta(
            nombre="Tacos al Pastor",
            descripcion="Un platillo tradicional mexicano con carne de cerdo adobada, acompañada de piña.",
            ingredientes=[
                "500g de carne de cerdo", "1 piña", "2 dientes de ajo", "Chile guajillo", 
                "Tortillas de maíz", "Cebolla", "Cilantro", "Limón", "Salsa",
            ],
            pasos=[
                "Marinar la carne con chile guajillo, ajo y especias", 
                "Cortar la piña en rodajas", 
                "Asar la carne en un trompo o en un sartén", 
                "Servir en tortillas calientes con cebolla, cilantro, piña y salsa",
            ],
        ),
        Receta(
            nombre="Enchiladas Verdes",
            descripcion="Enchiladas rellenas de pollo bañadas en salsa verde, servidas con crema y queso.",
            ingredientes=[
                "12 tortillas de maíz", "1 kg de pollo deshebrado", "500g de tomates verdes", 
                "1/4 de cebolla", "2 dientes de ajo", "Crema", "Queso fresco", "Aceite", "Sal",
            ],
            pasos=[
                "Cocer los tomates verdes, ajo y cebolla para hacer la salsa", 
                "Freír las tortillas en aceite", 
                "Rellenar las tortillas con pollo y enrollarlas", 
                "Bañar las enchiladas con la salsa verde y hornearlas por 10 minutos", 
                "Servir con crema y queso fresco",
            ],
        ),
        Receta(
            nombre="Sopa de Lima",
            descripcion="Una sopa ligera y fresca de pollo, con un toque de lima, típica de la región de Yucatán.",
            ingredientes=[
                "1 pollo entero", "1 cebolla", "2 dientes de ajo", "2 limas", "Tortillas de maíz", 
                "Cilantro", "Aceite", "Sal", "Pimienta",
            ],
            pasos=[
                "Cocer el pollo en agua con cebolla y ajo", 
                "Freír las tortillas en tiras pequeñas", 
                "Exprimir el jugo de las limas", 
                "Añadir el pollo desmenuzado a la sopa", 
                "Servir la sopa con las tiras de tortilla, cilantro y jugo de lima",
            ],
        ),
    ]

class Resultado(ComplexModel):
    """Representa el resultado de una operación de depósito o retiro. Opcionalmente incluye el saldo actual."""
    status = Unicode
    message = Unicode
    recetas = Array(Receta)

    @classmethod
    def ok(cls, mensaje, nuevo_recetario):
        """Crea un objeto Resultado con status 'OK', un mensaje y el saldo actual."""
        return cls(status='OK', message=mensaje, recetas = nuevo_recetario)
    
    @classmethod
    def error(cls, mensaje, nuevo_recetario):
        """Crea un objeto Resultado con status 'ERROR' y un mensaje."""
        return cls(status='ERROR', message=mensaje, recetas = nuevo_recetario)
    
class RecetaService(Service):
    """Servicio web de Recetas."""

    @srpc(_returns=Array(Receta))
    def recetas():
        """Regresa el listado completo de recetas."""
        return _recetas_db


    @srpc(String,_returns=Resultado)
    def ver_receta(nombre):
        """Regresa una receta del listado de Recetas basada en su nombre.

        Devuelve un error en caso de no encontrar una receta con el nombre dado.

        Parametros:
            nombre -- Nombre de la receta que se desea recuperar.
        """
        receta_existente = None
        for receta in _recetas_db:
            if receta.nombre == nombre:
                receta_existente = receta
                break

        if not receta_existente:
            return Resultado.error("No se encontro una receta con el nombre dado.", _recetas_db)

        return Resultado.ok(f"Se encontro la receta con el nombre {nombre}.", [receta_existente])
    

    @srpc(String,_returns=Resultado)
    def buscar_por_ingrediente(ingrediente):
        """Regresa un listado de Recetas que contengan ingredientes que contengan nombres con la cadena dada.

        Devuelve un listado vacío en caso de no encontrar recetas.

        Parametros:
            ingrediente -- Nombre del ingrediente que se busca en las recetas.
        """
        recetas_existentes = []
        for receta in _recetas_db:
            for ingrediente_en_receta in receta.ingredientes:
                if ingrediente.lower() in ingrediente_en_receta.lower():
                    recetas_existentes.append(receta)
                    break

        if not recetas_existentes:
            return Resultado.ok("No se encontraron recetas con el ingrediente dado.", [])
        if len(recetas_existentes)==1:
            Resultado.ok(f"Se encontro una receta con el ingrediente {ingrediente}.", recetas_existentes)

        return Resultado.ok(f"Se encontraron {len(recetas_existentes)} recetas con el ingrediente {ingrediente}.", recetas_existentes)
    

    @srpc(String, String, Array(String), Array(String),_returns=Resultado)
    def registrar(nombre, descripcion,ingredientes, pasos):
        """Agrega una receta nueva al listado de Recetas.

        Parametros:
            nombre -- Nombre de la receta.
            descripcion -- Descripción del platillo.
            ingredientes -- Listado de ingredientes necesarios para la receta.
            pasos -- Listado de pasos a seguir para cocinar la receta.
        """
        receta_existente = None
        for receta in _recetas_db:
            if receta.nombre == nombre:
                receta_existente = receta
                break

        if receta_existente:
            return Resultado.error("Ya existe una receta con el nombre dado.",_recetas_db)
        
        nueva_receta = Receta(nombre = nombre, descripcion = descripcion, ingredientes =  ingredientes, pasos = pasos)
        _recetas_db.append(nueva_receta)
        return Resultado.ok("Se agrego receta nueva",_recetas_db)


    @srpc(String, String, Array(String), Array(String),_returns=Resultado)
    def actualizar(nombre, descripcion,ingredientes, pasos):
        """Actualiza una receta del listado de Recetas basa en el nombre.

        No ingresa los datos en caso de que no exista una receta con el nombre dado.

        Parametros:
            nombre -- Nombre de la receta al ser actualizada.
            descripcion -- Descripción del platillo.
            ingredientes -- Listado de ingredientes necesarios para la receta.
            pasos -- Listado de pasos a seguir para cocinar la receta.
        """
        receta_existente = None
        for receta in _recetas_db:
            if receta.nombre == nombre:
                receta_existente = receta
                break

        if receta_existente:
            receta_existente.descripcion = descripcion
            receta_existente.ingredientes = ingredientes
            receta_existente.pasos = pasos
            return Resultado.ok("Se actualizo la receta correctamente.", _recetas_db)
        
        nueva_receta = Receta(nombre=nombre, descripcion=descripcion, ingredientes=ingredientes, pasos=pasos)
        _recetas_db.append(nueva_receta)
        return Resultado.error("No se encontro la receta con el nombre dado.", _recetas_db)
    

    @srpc(String,_returns=Resultado)
    def borrar(nombre):
        """Borra una receta del listado de Recetas basa en el nombre.

        Devuelve un error en caso de no encontrar una receta con el nombre dado.

        Parametros:
            nombre -- Nombre de la receta que se desea borrar.
        """
        receta_existente = None
        for receta in _recetas_db:
            if receta.nombre == nombre:
                receta_existente = receta
                break

        if not receta_existente:
            return Resultado.error("No se encontro una receta con el nombre dado.", _recetas_db)

        _recetas_db.remove(receta_existente)
        return Resultado.ok(f"Se borro la receta con nombre {nombre}.", _recetas_db)
    
spyne_app = Application(
    services=[RecetaService],
    tns='com.rgarcia.recetas',
    name='Recetas',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(validator='lxml'),
)

wsgi_app = WsgiApplication(spyne_app)
