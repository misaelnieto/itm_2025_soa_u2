## Configuración de tu entorno de trabajo

Sigue esta guía para configurar tu entorno de desarrollo. Asumimos que tu
computadora esta corriendo una versión reciente de Windows 11.

Una vez que tengas configurado tu entorno de desarrollo podrás continuar a
desarrollar tu servicio web asignado.

## Paso 1: Winget

Abre una ventana de PowerShell o Windows Terminal y escribe el comando `winget`. Si en la pantalla ves un mensaje parecido a este>

> `wingeto : El término 'wingeto' no se reconoce como nombre de un cmdlet`

Deberas seguir la guía de instalación de winget desde la página de Microsoft https://learn.microsoft.com/es-es/windows/package-manager/winget/


## Paso 2: Instalando y configurando git

Instala `git` con el siguiente comando:

```powershell
winget install -e --id Git.Git
```

Una vez instalado debes configurar `git` con tu nombre y correo electronico

```powershell
git config --global user.name "Fulano Fernandez"
git config --global user.email ffernandez@example.com
```

!!! note "Usa el email que registraste en GitHub"
    Usa el email que registraste en GitHub para que se asocien los *commits* correctamente a tu nombre de usuario.

La manera más confiable para interactuar con repositorios de github es mediante
el protocolo SSH. Para eso tienes que generar un par de llaves público/privadas
y luego registrar la llave pública en tu cuenta de GitHub.

Para generar la llave por primera vez, ejecuta el siguiente comando en powershell:

```powershell
ssh-keygen -t ed25519 -C "ffernandez@example.com"
```

- Cuando se te pregunte en dónde guardar la llave, solo presiona enter.
- Cuando se te pregunte proporcionar una frase de paso, solo presiona enter.

Ejemplo de la creación de una llave para Fulano Fernandez

```PowerShell
PS C:\> ssh-keygen -t ed25519 -C "ffernandez@example.com"
Generating public/private ed25519 key pair.
Enter file in which to save the key (C:\Users\ffernandez/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in C:\Users\ffernandez/.ssh/id_ed25519
Your public key has been saved in C:\Users\ffernandez/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:3uwn3gOEs0WCM1pVHVfZi2+MUhUvB7Mz0gKKT6DFwt0 ffernandez@example.com
The key's randomart image is:
+--[ED25519 256]--+
|   . oo+..o...+o=|
|    ooBoE....o *o|
|    .+.oo+  o O +|
|    .  oo o  = * |
|        S=  . +  |
|       ..o.. . + |
|        . o.. .  |
|         ...o    |
|         .oo..   |
+----[SHA256]-----+
```

Con esto, se habrá creado un par de archivos en `C:\Users\ffernandez/.ssh/`:

```PowerShell
 dir C:\Users\ffernandez/.ssh/


    Directorio: C:\Users\ffernandez\.ssh


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----     19/12/2024  06:28 p. m.            208 config
-a----     16/12/2024  08:38 p. m.            399 id_ed25519
-a----     16/12/2024  08:38 p. m.             96 id_ed25519.pub
-a----     10/01/2025  03:38 p. m.           1948 known_hosts
-a----     10/01/2025  03:38 p. m.           1217 known_hosts.old
```

Los dos archivos generados fueron `id_ed25519` y `id_ed25519.pub`, que son la
llave privada y la llave pública, respectivamente.

Ahora el siguiente paso es abrir el archivo de la llave pública, copiar el texto
que cotiene para usarlo en la configuración de tu cuenta de github. Puedes abrir
el archivo de la llave pública fácilmente usando notepad desde la línea de
comandos.

```powershell
notepad C:\Users\ffernandez/.ssh/id_ed25519.pub
```

Inmediatamente después se abrirá la ventana de Notepad y podrás copiar el texto.

El siguiente paso es abrir la configuración de tu cuenta de GitHub en la sección
de llaves SSH (https://github.com/settings/keys).

Presiona el botón **"New SSH Key"**, agrega un título descriptivo y pega el contenido de la llave pública en el cuadro de texto **Key**.


Finalmente, para probar tu llave corre el siguiente comando:

```powershell
ssh -T git@github.com
```

Deberías ver el siguiente mensaje:

```
Hi ffernandez! You've successfully authenticated, but GitHub does not provide shell access.
```

## Clona el repositorio y crea tu rama de trabajo


```powershell
git clone git@github.com:misaelnieto/itm_2025_soa_u2.git
cd itm_2025_soa_u2
git switch --create fferndez-servicioweb
```


### Instalación de python, `uv` y entorno virtual

Sigue el proceso de instalación de `uv` desde la página oficial https://docs.astral.sh/uv/.

Una vez que hayas instalado y configurado `uv`, cincroniza las dependencias y versión de python con el siguiente comando:

```powershell
uv sync
```

La primera vez que corras este comando, `uv` descargará la versión de Python
adecuada, creara un entorno virtual e instalará todas las dependencias
necesarias para tus prácticas.


## Arrancando el servidor web de desarrollo

```
uv run webservice --debug
```

Cuando hagas cambios en tu código, el servidor reiniciará automáticamente. Recuerda revisar los errores y advertencias en la terminal donde estas ejecutando el servidor. Presiona `Ctrl`+`C` para terminar la ejecución del servidor de pruebas.

## Corriendo las pruebas con pytest

El siguiente comando correrá todas las pruebas contenidas en el módulo `tests`

```
uv run pytest
```

Si solo deseas correr las pruebas las pruebas contenidas en tu módulo asignado de pruebas, simplemente proporciona la ruta al módulo que contiene la prueba que deseas correr. Por ejemplo, si tu prueba esta en `tests/test_ffernandez.py`, el comando de `pytest` sería:


```
uv run pytest tests/test_ffernandez.py
```

También es posible correr una sola prueba dentro de un módulo de la siguiente manera:


```
uv run pytest tests/test_ffernandez.py::test_abc
```

Consulta la documentación de `pytest` en https://docs.pytest.org/en/stable/ para obtener más información acerca de su uso y sus diferentes maneras de invocar y depurar pruebas.


### Corriendo el analizador de código estático

WIP

```
uv run ruff check .
```

### Editor de código

Puedes usar el editor de código de tu preferencia. El profesor usa Visual Studio Code y ha pre-configurado el entorno para que te sea más fácil desarrollar tu trabajo.



## Referencia de la herramienta de línea de comandos `webservice`


::: mkdocs-click
    :module: webservice.app
    :command: main
