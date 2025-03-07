# Proyecto Productos

## Módulo `productos`

::: webservice.dramos.servicio

El servicio expone los siguientes métodos SOAP:

## Métodos 
### `listado()`

Obtiene la lista de productos registrados.

### `Retorno:`

Array(Producto): Una lista de objetos Producto.

### `registrar(nombre: String, categoria: String, precio: String)`

Registra un nuevo producto.

### `Parámetros:`

nombre: Nombre del producto.

categoria: Categoría del producto.

precio: Precio del producto.

### `Retorno:`

"Producto registrado" si el registro es exitoso.

### `eliminar(nombre: String)`

Elimina un producto por su nombre.

### `Parámetros:`

nombre: Nombre del producto a eliminar.

### `Retorno:`

"Producto eliminado correctamente" si el producto existía y se eliminó.

"Producto no encontrado" si el producto no existe.

### `actualizar(nombre: String, nueva_categoria: String, , nuevo_precio: String)`

Actualiza la categoría de un producto existente.

### `Parámetros:`

nombre: Nombre del producto a modificar.

nueva_categoria: Nueva categoría a asignar.

nuevo_precio: Nuevo precio del producto.

### `Retorno:`

"Producto actualizado correctamente" si la actualización fue exitosa.

"Producto no encontrado" si el producto no existe.

## `Estructura del Código`

### `Definición de Clases`

Producto

Modelo de datos que representa un producto con los siguientes atributos:

nombre: String

categoria: String

precio = String  

_productos

Lista inicial con productos precargados:
   _productos = [
    Producto(nombre="Coca-cola", categoria="Refresco", precio="15"),
    Producto(nombre="Sabritas", categoria="Fritura", precio="10"),
]

### `Configuración del WebService`

Se usa spyne.Application para definir el servicio:

spyne_app = Application(
    services=[ProductosService],
    tns='com.dramos.productos',
    name='Productos',
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(validator="lxml"),
)

wsgi_app = WsgiApplication(spyne_app)