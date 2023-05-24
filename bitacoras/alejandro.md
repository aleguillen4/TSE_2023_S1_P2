### Previo al 3 de mayo
Investigación de aspectos iniciales a tomar en cuenta para buildear la rpi, principalmente para hacerse una idea del proceso necesario a la hora de sintetizar una imagen

Se realiza una imagen mínima a nivel local, se logra trasladar la imagen a la tarjeta sd con el comando 

```
sudo dd bs=4M if=path_a_la_imagen of=/dev/sda (path por default en la sd) conv=fsync
```

### 3 de Mayo
Se trabaja localmente el build de las imágenes, es decir, en mi máquina Ubuntu

Como premisa inicial se utiliza el release de kirkstone, parecía un paso común en algunos tutoriales 

Se encuentra que kirkstone no es compatiblle con la imagen a sintetizar, por lo que se traslada a mickledore según el mensaje de error

Se agrega manualmente la siguiente linea al local.conf para evitar un nuevo error detectado
```
LAYERSERIES_COMPAT_raspberrypi = "mickledore"
```
Se intenta utilizar el release mickledore, pero al final no funciona, acá algunos parámetros utilizados en ese momento

```
git checkout -t origin/mickledore -b mymickledore
git clone git://git.yoctoproject.org/poky
git checkout -t origin/mickledore -b mymickledore
```
A pesar de que en el archivo bblayer se agregó meta-tensorflow-lite el build no estaba encontrando el path, por lo que se agrega manualmente con el siguiente comando
```
bitbake-layers add-layer ../../meta-tensorflow-lite/
```
### Periodo entre 3 y 8 de Mayo
Durante estos días se transicionó entre las imágenes que se fueran a sintetizar. Primero se había pensado en una x11 o una sato, sin embargo estas fallaban después de horas de estar buildeándose

En mi máquina local tenía asignadas 130 GB a la partición de Linux, sin embargo esto fue un impedimento, utilizando gparted y un usb con una imagen de ubuntu utilicé gparted para asignar más recursos a la partición de Linux, le asigné 256 GB.

A pesar de el aumento de almacenamiento dispobible, las imágenes sato y x11 utilizaban todos los recursos, por lo que se decide utilizar una imagen mínima

### 8 de Mayo
Se agregan algunas dependencias a el build para intentar bootear la rpi2 utilizando una imagen mínima y empezar con el testing

```
(local.conf)
MACHINE ??= "raspberrypi2"
GPU_MEM = "16"
IMAGE_FSTYPES = "tar.xz ext3 rpi-sdimg"
VIDEO_CAMERA = "1"
IMAGE_INSTALL:append = " python3 python3-numpy python3-tensorflow-lite cpp-tensorflow-lite opencv vim"
(bblayers)
# POKY_BBLAYERS_CONF_VERSION is increased each time build/conf/bblayers.conf

# changes incompatibly
POKY_BBLAYERS_CONF_VERSION = "2"
BBPATH = "${TOPDIR}"
BBFILES ?= ""
BBLAYERS ?= " \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-poky \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-yocto-bsp \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-raspberrypi \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-openembedded \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-tensorflow-lite \
  "
```
### 9 de Mayo
La imagen mínima, de la misma manera, luego de horas de estar sintetizándose, faltando un 5% del build fallaban, esto pasó en varias ocasiones, y no se encuentra un error a nivel de local.conf o bblayers, ni de dependencias. 

Luego de reiterados fallos en la síntesis de la imagen, después de mucho tiempo en debugging, y realizando diferentes pruebas en la máquina local; no se encuentra un problema evidente, por lo que decido compartir mi progreso relacionado a yocto, para que Daniel y Rachell intenten lo mismo, para descartar que sea mi máquina. 
### Período entre 10 y 15 de Mayo
Se cambian diferentes parámetros en el build, en general debugging de problemas en los comandos o similar, se elimina la carpeta poky y se clona pero con el release langdale. Se intentan nuevos Builds y se busca información en tutoriales. 

### 16 de Mayo
Hasta este momento he trabajado con mi máquina con Ubuntu nativo y prestaciones regulares (corei5 octava, 16Gb de ram, 256Gb almacenamiento) decido configurar la máquina virtual (previamente no me había funcionado la conexión por ssh) desde cero, crear un alias "runvm" para conectarme a la VM de azure, realizo el proceso de crear y montar un nuevo disco de 256 GB y en general realizo los cambios necesarios para trabajar los builds a nivel de VM. 

Finalmente se utiliza el realese de langdale, a continuación se ve el flujo de comandos en la máquina virtual

```
git clone -b langdale https://github.com/yoctoproject/poky.git
cd poky/
git clone -b langdale git://git.yoctoproject.org/meta-raspberrypi
git clone -b langdale https://github.com/NobuoTsukamoto/meta-tensorflow-lite.git
git clone -b langdale https://github.com/openembedded/meta-openembedded.git
source oe-init-build-env
vim conf/bblayers.conf 
vim conf/local.conf 
sudo apt-get install build-essential
sudo apt-get update
sudo apt-get install chrpath diffstat zstd
source oe-init-build-env 
bitbake core-image-base
```
Los archivos de configuración son compartidos en el repositorio luego de que se pudiera bootear la imagen mínima. 

Se utiliza core-image-base en vez de la mínima, debido a que esta sí presenta compatibilidad con la cámara y en general con el protocolo USB. 

```
# POKY_BBLAYERS_CONF_VERSION is increased each time build/conf/bblayers.conf
# changes incompatibly
POKY_BBLAYERS_CONF_VERSION = "2"

BBPATH = "${TOPDIR}"
BBFILES ?= ""

BBLAYERS ?= " \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-poky \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-yocto-bsp \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-raspberrypi \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-openembedded/meta-python \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-openembedded/meta-oe \
  /home/alejandro7570/Documents/2023_1S/Taller_de_sistemas_embebidos/yocto/poky/meta-tensorflow-lite \
  "
```

```
# This sets the default machine to be qemux86-64 if no other machine is selected:
FORTRAN:forcevariable = ",fortran"
MACHINE ??= "raspberrypi2"
GPU_MEM = "16"
IMAGE_FSTYPES = "tar.xz ext3 rpi-sdimg"
VIDEO_CAMERA = "1"
IMAGE_INSTALL:append = " python3 python3-numpy python3-tensorflow-lite libtensorflow-lite opencv vim"

```
### 17 de Mayo
Ya con la rpi2 booteada se empieza a testear la cámara con un script simple que utilizaba opencv. Se logra tomar una imagen por lo que se pasa a trabajar en la conexión ssh

### 19 de Mayo
Se intenta realizar la conexión SSH luego de conseguir un cable ethernet. Donde vivo no tengo disponibilidad para conectar la rpi al router, por lo que tengo que conectarla directamente a la computadora. La computadora no logra conectarse con la rpi2, por lo que empieza una pequeña etapa de investigación. 

### 22 de Mayo
Se actualizan las dependecias en la imagen de la rpi2 para descartar problemas de dependencias en la rpi2

```
FORTRAN:forcevariable = ",fortran"
MACHINE ??= "raspberrypi2"
GPU_MEM = "16"
IMAGE_FSTYPES = "tar.xz ext3 rpi-sdimg"
VIDEO_CAMERA = "1"
RPI_CAMERA = "1"
DISTRO_FEATURES:append = "v4l2 ssh-server-openssh systemd"
IMAGE_INSTALL:append = " \
        python3-picamera \
        git \
        python3-pip \
        python3-pygobject \
        python3-paramiko \
        openssh \
        picamera-libs \
        v4l-utils \
        usbutils \
        python3 \
        python3-numpy \
        python3-tensorflow-lite \
        libtensorflow-lite \
        opencv \
        vim \
        ssh \
        openssh-sftp-server \
        openssh-keygen \
        systemd"
VIRTUAL-RUNTIME_init_manager = "systemd"
VIRTUAL-RUNTIME_initscript = "systemd-compat-units"
```
Se realizan consultas con diferentes compañeros, sin embargo las dependencias, la imagen y la rpi2 no dejan ver un problema evidente, por lo que, una vez más, se intenta descartar que mi máquina sea el problema, por lo que le entrego la rpi2 a Rachel 
