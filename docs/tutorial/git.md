# Paso 2: Git

## Instalación

Instala `git` con el siguiente comando:

```powershell
winget install -e --id Git.Git
```

## Configuración de nombre y correo

Una vez instalado debes configurar `git` con tu nombre y correo electrónico.

```powershell
git config --global user.name "Fulano Fernandez"
git config --global user.email ffernandez@example.com
```

!!! note "Usa el email que registraste en GitHub"
    Usa el email que registraste en GitHub para que se asocien los *commits* correctamente a tu nombre de usuario.

## Configuración de SSH

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
