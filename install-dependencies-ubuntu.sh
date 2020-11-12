
sudo add-apt-repository -y ppa:ubuntugis/ppa
sudo apt-get -y update
sudo apt-get -y install gdal-bin
sudo apt-get -y install libgdal-dev
sudo apt-get -y install libspatialindex-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
