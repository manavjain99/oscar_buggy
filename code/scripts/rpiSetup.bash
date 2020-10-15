#!/bin/bash

# Author: Param Deshpande
# Date Created:  Wed 7 Oct 15:16:26 IST 2020
# Description: Install all essentials to run this project on a Rpi.
# Date Modified:  Wed 7 Oct 15:16:26 IST 2020
# License :
# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# Param Deshpande wrote this code. As long as you retain this 
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return.
# ------------------------------------------------------------
#


###################  DEFINE YOUR VARS HERE ###################


##################### START YOUR CODE HERE ################### 

echo 
echo please enter your password 
echo 'this script will install most of the essentials on this Rpi needed for the project to run...'

[ `whoami` = root ] || exec sudo su -c $0 root

echo 'Please wait for a few moments , dont press any keys ......'
yes Y | apt-get update 
yes Y | apt-get upgrade

# references : https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/
yes Y | apt-get install build-essential cmake pkg-config
yes Y | apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
yes Y | apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
yes Y | apt-get install libxvidcore-dev libx264-dev
yes Y | apt-get install libfontconfig1-dev libcairo2-dev
yes Y | apt-get install libgdk-pixbuf2.0-dev libpango1.0-dev
yes Y | apt-get install libgtk2.0-dev libgtk-3-dev
yes Y | apt-get install libatlas-base-dev gfortran
yes Y | apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
yes Y | apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
yes Y | apt-get install python3-dev
yes Y | wget https://bootstrap.pypa.io/get-pip.py
yes Y | python get-pip.py
yes Y | python3 get-pip.py
yes Y | rm -rf ~/.cache/pip

# making pip and python versions , as pip3 & python3 
echo 'text' | sudo tee -a ~/.bashrc
echo 'alias python=python3' | sudo tee -a ~/.bashrc
echo 'alias pip=pip3' | sudo tee -a ~/.bashrc
echo 'export PATH=$PATH:/home/pi/.local/bin' | sudo tee -a ~/.bashrc



source ~/.bashrc

yes Y | pip3 install virtualenv virtualenvwrapper
yes Y | pip3 install opencv-contrib-python==4.1.0.25



# exit from root shell.
exit

#read

####################### END OF SCRIPT #######################