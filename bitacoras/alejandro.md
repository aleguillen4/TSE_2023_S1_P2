### Previo al 3 de mayo
Investigación de aspectos iniciales a tomar en cuenta para buildear la rpi, principalmente para hacerse una idea del proceso necesario a la hora de sintetizar una imagen

### 3 de Mayo
Se trabaja localmente el build de las imágenes, es decir, en mi máquina Ubuntu
Como premisa inicial se utiliza el release de kirkstone, parecía un paso común en algunos tutoriales 

Se encuentra que kirkstone no es compatiblle con la imagen a sintetizar, por lo que se traslada a mickledore según el mensaje de error
Se agrega manualmente la siguiente linea al local.conf para evitar el error
```
LAYERSERIES_COMPAT_raspberrypi = "mickledore"
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



