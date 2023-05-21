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



