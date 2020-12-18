# sudo apt-get install python3.6 python3.6-dev python3-pip
# sudo add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
sudo add-apt-repository --yes ppa:ubuntugis/ppa
sudo apt --yes update
sudo apt-get --yes install gdal-bin libgdal-dev libspatialindex-dev
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
