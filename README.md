Practica2IV
===========

Creando jaulas para aplicaciones
--------------------------------

En esta práctica he creado dos aplicaciones sobre una jaula que
esta ejecutando el sistema operativo CentOS-6. Una de las aplicaciones
permite crear, editar, y visualizar los issues de la asignatura, mientras
que la segunda aplicación permite cambiar el lugar de la cuenta de Github
a `Granada`. La primera aplicación se crea usando ```python``` y la segunda
con ```node```.

Para la creación la aplicación en la jaula, he seguido los siguientes
pasos:

> 1. Crear la jaula y hacer ```chroot``` sobre ella.
> 2. Hay que crear un usuario dentro de la jaula asi tenemos acceso
remoto a dicha jaula
> 3. Dentro del jaula, se ha instalado los paquetes necesarios para crear
y ejecutar la aplicación.
> 4. Después de ver que las aplicaciones de han desplegado en la jaula,
subimos el código a Github.


* Para esta práctica he creado un jaula con el programa [rinse][1],
que permite la instalación de un sistema mínimo RPM, como fedora, centos, rhel.
He optado por CentOS debido a que es una de las distribuciones más usadas
para servidor de aplicaciones.

En la siguiente imagen se puede visualizar como se ha creado la jaula:

!["Creación de la jaula"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/crearjaula.png)

Después que rinse haya descargado los paquetes necesarios para la instalación
se hace un chroot, para cambiar el directorio de root a dicha jaula

```sh
chroot /home/ivp2/
```
* Aunque podemos entrar a la jaula, sería beneficial tener un usuario
que esta dentro de la jaula, que puede acceder de manera remota.

Antes de entrar a la jaula creamos el usuario usando el siguiente comando:

```sh
sudo useradd -s /bin/bash -m -d /home/ivp2/./home/p2user -c
"CentOS6 josecolella" -g users p2user
```

Después de crear el usuario, hay que definir ciertas reglas para
que cuando se haga un acceso remoto.

El fichero que hay que modificar es ```/etc/ssh/sshd_config```. En dicho
fichero hay que definir el directorio que se aplicará el chroot.

En la siguiente imagen podemos ver el cambio hecho en dicho fichero.

!["Cambios en /etc/ssh/sshd_config"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/cambiosensshdconfig.png)


Después de haber hecho dicha configuración, se reinicia el servicio usando:

```sh
sudo service ssh restart
```

Ahora se define unas reglas para restringir al usuario ```p2user```

```sh
sudo usermod -G ssh p2user
sudo usermode -s /bin/bash p2user
sudo chown root:root /home/ivp2/./home/p2user/
sudo chmod 0755 /home/ivp2/./home/p2user
```

Lo que se ha hecho con los anteriores comandos es modificar atributos del
usuario ```p2user```

Ya definido dichas reglas para el usuario, hay que definir la contraseña para dicho usuario, usando ```sudo passwd josecolella```.

Para acceder usamos el siguiente comando:

```sh
ssh p2user@192.168.1.24
```

Como podemos ver en la siguiente imagen el usuario puede acceder mediante ssh
pero esta limitado en lo que puede hacer como vemos en la segunda imagen.

!["ssh de p2user"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/sshp2user.png)

!["Restriciones sobre p2user"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/restrictuser.png)

Cuando estamos dentro de la jaula, el usuario ya no tiene permiso a visualizar cosas
fuera.

* Estando dentro de la jaula, hay que tener en cuenta que tenemos un sistema
mínimo, y que hay que instalar todos los paquetes para crear y ejecutar la
aplicación.

Las aplicaciones que he creado requiere python, python3, node.
Antes de instalar dichos paquetes, hay que instalar unos paquetes de sistema y
agregar EPEL, que es un repositorio que contiene un multitud de paquetes para
distribuciones que usan RPM.

Siguiendo los siguientes comandos:

```sh
wget http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -Uvh  epel-release-6*.rpm
```
he instalado EPEL

A continuación instalamos unas herramientas essentiales
para coger paquetes, escribir la aplicación, y compilar
los modulos de instalación (autoconf,automake,gcc,g++,...)

```sh
yum update
yum install wget curl vim sudo
yum -y groupinstall "Development Tools"
```

Para instalar python3, primero he descargado el comprimido de la página
oficial, como se ve en la siguiente imagen:

!["Descargar el comprimido de python"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/installingpython.png)

Después de haber descargado el comprimido, he seguido los siguientes
comandos:

```sh
tar xfz Python-3.3.2.tar.bz
cd Python-3.3.2/
./configure
make
make install
```

Ya instalado el python, hay que instalar ```pip```, que es el gestionador
de modulos de python. Para instalar ```pip```, se ejecuta el siguiente comando:

```sh
yum install python-pip
```

Ya instalado el ```pip```, hay que descargarse el [modulo][3] para poder interactuar
con las [API de Github][2].

```sh
pip install githubpy
```

Ya instalado el modulo, se puede crear la aplicación. Dicha aplicación permite
crear, editar, y visualizar los issues abiertos de la asignatura.

El código se puede visualizar [aquí][4].

Para probar que trabaja bien la aplicación, he creado un issue para una
aplicación de prueba, después cambiando los datos del repositorio y organización.

```sh
python IVissue.py josecolella [password] create "Rails 4" "update to Rails 4"
```

En la imagen anterior se puede ver como se interacciona con la aplicación.

!["Se puede ver que se ha creado el issue"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/success.png)

### *Cambio*

La aplicación de python se ha cambiado para que se pueda crear issues con labels
como ```question```, ```bug```, etc...

En la siguiente imagen, podemos ver como se puede crear un issue con label y asignarlo
a [JJ][9].

!["Aplicación ejecutada con asignee e issue"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/PythonIssueLabel.png)

Para la segunda aplicación, en la cual necesitamos ```node```, he descargado
el paquete oficial. He seguido los siguientes pasos para instalar ```node```

```sh
wget http://nodejs.org/dist/v0.10.21/node-v0.10.21.tar.gz
tar zxf node-v0.10.21.tar.gz
cd node-v0.10.21
./configure
make
make install
```

Después de haber instalado node, hay que instalar el modulo
para que node pueda interactuar con las [APIs de Github][2].

El modulo se puede conseguir en [github][5], y tiene una buena
documentación de uso. Para instalar se usa el gestionador de modulos
de node; npm.

!["Instalación del modulo para interactuar con API Github"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/npminstallgithub.png)

Ya instalado el modulo, ya se puede escribir y ejecutar la aplicación.
La aplicación basicamente cambia el lugar de ubicación del usuario en
github.

!["Código de la aplicación"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/changinglocation.png)


Podemos ejecutar la aplicación se efecta el siguiente comando, como
se puede ver en la siguiente imagen:

!["Ejecución de la aplicación"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/commandline.jpg)

```sh
node changinglocation.js [nombreUsuario][Contraseña]
```

La aplicación coge dos parametros de la linea de comando. El
primer parametro sirve como el nombre de usuario de github, y
el segundo es la contraseña.


| Argumentos |           |
| --- | ----------------- |
|  1  | nombre de usuario |
|  2  |        contraseña |


Para probar que la aplicación sirve, primero verificamos que en github, se
enseñe vacio el campo de "Location", como en la siguiente imagen.

!["Campo vacio de location"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/location.png)

También se puede verificar revisando el perfil, como se puede ver en la
siguiente imagen:

!["Perfil sin location"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/withoutlocation.png)

Después de hacer la ejecución de la aplicación, podemos visualizar en el perfil,
que nuestro usuario tiene un lugar.

!["Perfil con location"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/withlocation.png)

### **Cambio**

Se ha hecho un cambio a la aplicación creada para cambiar la ubicación indicada
en GitHub. En vez de usar linea de comando, he creado una interfaz web con un
formulario simple, en el cual el usuario mediante un formulario ingresa su nombre de usuario
y contraseña en los campos correspondientes.
La aplicación modificada se puede encontrar [aquí][8]

En la siguiente imagen se puede visualizar la interfaz web que proporciona dicha
aplicación.

!["Interfaz web de la aplicación node"](https://raw.github.com/josecolella/Practica2IV/master/Screenshots/nodeapplication.png)


Conclusión
----------

Usar jaulas para la creación y despliegue de aplicaciones es un beneficio para un
desarrollador debido a que los pone en control de su sistema de despligue.
El desarrollador puede definir precisamente como contruir su "application stack",
comenzando de un sistema minimalista. Además el administrador del sistema
no se tiene que preocupar ya que el desarrollador esta enjaulador en su sistema.
La herramienta rinse también le veo un gran beneficio ya que crea un sistema
minimalista facilmente, sin preocuparse mucho en las configuraciones.

Este sistema de jaulas no es tan ágil en despliegue como los PaaS visto
en la primera sección, ya que en ese instante solo había que preocuparse
de definir las dependencias grandes del proyecto. Para las jaulas minimas,
hay que instalar las herramientas para instalar la pila de aplicaciones
necesaria para ejecutar la aplicación, cosa que requiere tiempo del
desarrollador.

Licencía
========

Licencía de GNU GENERAL PUBLIC LICENSE. Ver [LICENSE][6] para más detalles.


[1]: http://www.steve.org.uk/Software/rinse/
[2]: http://developer.github.com/v3/
[3]: https://github.com/michaelliao/githubpy
[4]: https://github.com/josecolella/Practica2IV/blob/master/IVissue.py
[5]: https://github.com/ajaxorg/node-github
[6]: https://github.com/josecolella/Practica2IV/blob/master/LICENSE
[7]: http://www.tldp.org/HOWTO/Chroot-BIND-HOWTO-2.html
[8]: https://github.com/josecolella/Practica2IV/blob/master/changingLocation.js
[9]: https://github.com/JJ
