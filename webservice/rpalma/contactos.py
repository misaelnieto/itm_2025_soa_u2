"""  
Este módulo contiene el proyecto de Agenda de contactos.  

Operaciones:  

- **Lista**: Muestra los contactos guardados.  
- **Buscar**: Busca en la agenda un contacto por su nombre.
- **Agregar**: Guarda un nuevo contacto en la agenda y muestra la lista actualizada.  
- **Editar**: Edita el nombre, el número de teléfono y/o el correo y muestra la lista actualizada.  
- **Eliminar**: Elimina un contacto de la lista y muestra la lista actualizada.  
"""
from spyne import AnyDict, Application, Array, ComplexModel, Integer, Service, String, srpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Contacto(ComplexModel):
    """Modelo que representa un contacto de la agenda.

    Cada contacto incluye un numero identificador, el nombre del contacto, un numero de telefono y un correo electronico.
    """
    num = Integer  
    nombre = String
    telefono = String
    correo = String


# Se hace una lista para la agenda con 4 contactos.  
agenda_db = [ 
    
    Contacto (
        num = 1,
        nombre = "Jair",
        telefono = "6861234567",
        correo = "a21490074@itmexicali.edu.mx",
    ),
    Contacto (
        num = 2,
        nombre = "Elena",
        telefono = "6868912345",
        correo = "a21490084@itmexicali.edu.mx",
    ),
    
    Contacto (
        num = 3,
        nombre = "Mariela",
        telefono = "6865552222",
        correo = "mariela@itmexicali.edu.mx",
    ),
    
    Contacto (
        num = 4, 
        nombre = "Diego",
        telefono = "6866236235",
        correo = "diego@itmexicali.edu.mx",
    ),
    
]

class ContactosService(Service):
    """Servicio web de Agenda."""

    @srpc(_returns=Array(Contacto))
    def lista():
        """Regresa el listado completo de contactos en la agenda."""
        return agenda_db
    
    @srpc(String(min_len=1, nillable=False), String, String,_returns=AnyDict)
    def agregar(nombre, telefono, correo):
        """Agrega un nuevo contacto a la agenda.

        Parametros:
        
        - **nombre**: Nombre de la persona.
        - **telefono**: Numero de telefono a 10 digitos.
        - **correo**: Correo electronico.
        """
        contacto_existente = None
        for contacto in agenda_db:
            if contacto.telefono == telefono or contacto.correo == correo:
                contacto_existente = contacto
                break

        if contacto_existente:
            return {"status":"ERROR", "mensaje": "Un contacto en la agenda ya tiene ese numero o correo"}
        
        #Buscar el num mas alto en la agenda y sumar 1.
        nvo_num = max((contacto.num for contacto in agenda_db), default=0) + 1
        
        nvo_contacto= Contacto(num = nvo_num, nombre = nombre, telefono = telefono, correo =  correo)
        agenda_db.append(nvo_contacto)

        return {"status":"OK", "mensaje": "Se agrego un nuevo contacto a la agenda", "nombre":nombre, "telefono":telefono, "correo":correo}
    
    @srpc(String(min_len=1, nillable=False),_returns=AnyDict)
    def buscar (nombre):
        """Busca el nombre de un contacto en la agenda y muestra los contactos encontrados.

        Parametros:
        
        - **nombre**: Nombre de la persona.
        """
        #Busca en toda la agenda por el nombre y si el nombre coincide, lo almacena.
        contactos_encontrados = []
        for contacto in agenda_db: 
            if contacto.nombre.lower() == nombre.lower():
                contactos_encontrados.append(contacto)
            
        if contactos_encontrados:
            return {"status":"OK", "mensaje": "Se encontraron contactos", "agenda": contactos_encontrados}
        
        return {"status":"ERROR", "mensaje": "No hubo resultados"}
    
    @srpc(Integer(nillable=False), String(min_len=1, nillable=False), String, String,_returns=AnyDict)
    def editar (num, nombre, telefono, correo):
        """Busca el num identificador de un contacto en la agenda y se editan los datos.

        Parametros:
        
        - **num**: numero identificador del contacto.
        - **nombre**: Nombre de la persona.
        - **telefono**: Numero de telefono a 10 digitos.
        - **correo**: Correo electronico.
        """
        if num is None:
            return {"status":"ERROR", "mensaje": "El numero identificador es obligatorio"}
    
        contacto_existente = None
        for contacto in agenda_db:
                if contacto.num == num:
                    contacto_existente = contacto
                    break
            
        if contacto_existente:
            contacto_existente.nombre=nombre
            contacto_existente.telefono=telefono
            contacto_existente.correo=correo
            return {"status":"OK", "mensaje": "El contacto se ha actualizado","num":num, "nombre":nombre, "telefono":telefono, "correo":correo}

        
        return {"status":"ERROR", "mensaje": "No existen contactos con ese numero identificador"}
    
    @srpc(Integer(nillable=False),_returns=AnyDict)
    def eliminar (num):
        """Busca el numero identificador de un contacto en la agenda y se elimina.
        
         Parametro:
        
        - **num**: numero identificador del contacto.
        """
        if num is None:
            return {"status":"ERROR", "mensaje": "El numero identificador es obligatorio"}
        
        contacto_existente = None
        for contacto in agenda_db:
                if contacto.num == num:
                    contacto_existente = contacto
                    break
            
        if contacto_existente:
            agenda_db.remove(contacto_existente)
            return {"status":"OK", "mensaje": "El contacto se ha eliminado!"}
        
        return {"status":"ERROR", "mensaje": "No fue posible eliminar porque no existen contactos con ese numero identificador"}

    
spyne_app = Application(
    services=[ContactosService],
    tns='com.rpalma.contactos',
    name='Contactos',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(validator='lxml'),
)

wsgi_app = WsgiApplication(spyne_app)