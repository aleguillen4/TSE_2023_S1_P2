# Reichel Morales Sánchez - Taller de embebidos-Proy2

### Domingo 16 de Abril

Investigación de como funciona tensorflow-lite, los diferentes tipos y bibliotecas que tiene este.

### Martes 2 de Mayo

Se empiezan a buscar al dependencias necesarias, por el momento se colocan las básicas como tensorflow-lite,python,numpy, opencv y vim.

Se utilizan los siguientes comandos para clonar los repositorios:
```
git clone -b langdale https://github.com/openembedded/meta-openembedded.git
git clone -b langdale https://github.com/openembedded/openembedded-core.git
git clones -b langdale https://github.com/NobuoTsukamoto/meta-tensorflow-lite

```

### Viernes 5 de Mayo

Se prueban modelos de clasificación de fotografías, sin embargo son muy inexactos, y no se entiende muy bien como modificarlos a lo que necesitamos en el proyecto.
Se estudia el que está en la págiana principal de Tensorflow.

### Jueves 11 de Mayo 

En el Local se indica que la MACHINE es raspberrypi2, se clona el respositorio para la raspb.

```
git clone -b langdale git://git.yoctoproject.org/meta-raspberrypi 
```

Se sigue con Yocto y se define la memoria del GPU, también definimos el formato de la imagen que vamos a usar en la raspberry.

```
GPU_MEM = "16"

IMAGE_FSTYPES = "tar.xz ext3 rpi-sdimg"

```
Se agrega al local dependencias necesarias para conectar la raspb y la computadora

```
IMAGE_INSTALL:append = " \
                 python3-pip \
                 python3-pygobject \
                 vim \
                 python3 \
                 python3-numpy \
                 openssh \                
                 openssl \
                 python3-tensorflow-lite libtensorflow-lite \
                 opencv \
                 "
```
### Viernes 19 de Mayo 

La imagen se estaba creando con:

```
Bitbake core-image-minimal

```
Pero estaba dando errores, y en las raspberrypi2, no estaba dando los resultados esperados, por lo que se decidió cambia a:

```
Bitbake core-image-minimal

```

Yocto dejó de correr la imagen por lo que se decide que se van a usar solo dos meta de Openembedded: `meta-python` y `meta-oe`.Los bblayers van quedando de la siguiente forma:

```
BBLAYERS ?= " \
  /pruebasyocto/poky/meta \
  /pruebasyocto/poky/meta-poky \
  /pruebasyocto/poky/meta-yocto-bsp \
  /pruebasyocto/meta-raspberrypi \
  /pruebasyocto/poky/meta-tensorflow-lite \
  /pruebasyocto/meta-python \
  /pruebasyocto/meta-oe \
 "
```
Sin embargo aun no se logra construir la imagen.

Se descubre que hay una carpeta con espacio pero está bloqueada, se realiza los siguientes comandos :

```
$ Sudo chown reimorales /dev/sda1
$ Sudo remount -o rw /dev/sda1
```
### Sábado 20 de Mayo 

Ale también estaba construyendo imágenes y me dijo que le agregara:

```
FORTRAN:forcevariable = ",fortran"
VIDEO_CAMERA = "1"
RPI_CAMERA = "1"
```
Según entiendo la de fortran es una variable que habilita soporte de compilaciól de código fortran para el entorno de Yocto.
Y según ChatGPT : Al establecer `VIDEO_CAMERA en "1"`, se indica que se debe incluir soporte para cámaras de video en la imagen generada por Yocto. Esto permitirá que las aplicaciones o componentes del sistema utilicen cámaras de video conectadas al sistema embebido.
Esta variable se utiliza específicamente en el contexto de Raspberry Pi. Al establecer `RPI_CAMERA en "1"`, se indica que se debe habilitar el soporte para la cámara oficial de Raspberry Pi en la imagen generada por Yocto. Esto permitirá que las aplicaciones o componentes del sistema utilicen la cámara Raspberry Pi conectada al sistema embebido.

Se agregaron más dependencias al local, por que la progra tiene varias librerias:

```
IMAGE_INSTALL:append = " \
                 example \
                 python3-pip \
                 python3-pygobject \
                 vim \
                 python3 \
                 python3-numpy \
                 openssh \
                 python3-picamera \
                 python3-h5py \
                 picamera-libs \
                 openssl \
                 libxcrypt \
                 libgfortran \
                 python3-tensorflow-lite libtensorflow-lite \
                 opencv \
		 python3-matplotlib \
                 "

```
### Domingo 21 de Mayo 

Se crea una layer llamada `meta-progra`
 
```
bitbake-layers create-layer meta-progra

```
El layer tiene archivos entre esos recipes-example/examples, cuando llegamos ahí solo vamos a tener un .bb qu es donde vamos a mandar a buscar los paquetes que necesitamos

```
├── conf
│   └── layer.conf
├── COPYING.MIT
├── README
├── recipes-example
    └── example
       └── example_0.1.bb
```

Se crea un archivo llamado files, por medio del comando :
 
```
mkdir files
```
En este vamos a tener 5 archivos: ` emotions_pi.py, haarcascade_frontalface_default.xml, inference.py , model.tflite , output.csv`

Los cuales debemos agregar al .bb

```
SUMMARY = "bitbake-layers recipe"
DESCRIPTION = "Recipe created by bitbake-layers"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://COPYING.MIT;md5=    "
SRC_URI = "file://emotions_pi.py \
	   file://haarcascade_frontalface_default.xml \
	   file://inference.py  \
	   file://model.tflite \
	   file://output.csv "

inherit python3native
do_install() {
	install -d ${D}${bindir}
	install -m 0755 emotions_pi.py ${D}${bindir}
	install -m 0755 haarcascade_frontalface_default.xml ${D}${bindir}
	install -m 0755 inference.py ${D}${bindir}
	install -m 0755 model.tflite ${D}${bindir}
	install -m 0755 output.csv ${D}${bindir}

}

```
Cada maquina tiene su propip md5, para poder encontrar el número exacto se debe correr el siguiente comando :

```
cd poky
cd build cd 
cd meta-progra
md5sum COPYING.MIT
```
Una vez que se corrió esto se muestra un numero el cual se va colocar en el md5= de la receta o .bb

También se agregó al local. conf la receta, del example y otras más que se van utlizar

```
IMAGE_INSTALL:append = " \
                 example \
                 python3-pip \
                 python3-pygobject \
                 vim \
                 python3 \
                 python3-numpy \
                 openssh \
                 python3-picamera \
                 python3-h5py \
                 picamera-libs \
                 openssl \
                 libxcrypt \
                 libgfortran \
                 python3-tensorflow-lite libtensorflow-lite \
                 opencv \
		 python3-matplotlib \
                 "
```

También se agregó al BBLAYERS

```
BBLAYERS ?= " \
  /pruebasyocto/poky/meta \
  /pruebasyocto/poky/meta-poky \
  /pruebasyocto/poky/meta-yocto-bsp \
  /pruebasyocto/meta-raspberrypi \
  /pruebasyocto/poky/meta-tensorflow-lite \
  /pruebasyocto/meta-python \
  /pruebasyocto/meta-oe \
  /pruebasyocto/poky/build/meta-progra \
  "
```
Alejandro no le servía la raspberry, me la da mañana

### Lunes 22 de Mayo 

Para cargar la imagen a la Raspberrypi2 por medio de Windows, se descargó un programa llamado Etcher recomendado por un compañero de clase:

```
https://balenaetcher.online
```
Se conecta la Raspberrypi2 con cable Ethernet al router de la casa, y se conecta la computadora a esa misma red.

Para poder conectar la compu a la raspberrypi2 se debe hacer por ssh, por lo que debemos conocer el IP de la raspb, ese se obtiene por medio de 'Ifconfig',una vez tenemos el IP,podemos conectarnos con el siguiente comando:

```
 ssh root@192.168.0.126
 
```
Una vez conectada se verifica que la progra funcione de manera correcta, pero se tuvieron que cambiar unas líneas sobre tensorflow-lite.

Ahora se prueba la progra que se corre en la máquina local llamada `GUI.py`, se le agregaron los siguientes parámetros:

```
username = 'root'
ip = '192.168.0.126' 
public_key = 'C:/Users/Rachell/.ssh/id_rsa'
remote_dir = '/usr/bin/'
```
De igual forma se crea una llave en la máquina local, la cuál se agrega a la imagen en la raspberrypi2.

Junto con Daniel se corrigieron varias cosas que dieron error al conectarla con un máquina remota.
