#!/bin/bash

# Author: Param Deshpande
# Date Created:  Wed Oct 14 15:36:50 IST 2020
# Description: this script will install all reqd pip packages to run the project , create a venv called env-oscar, this will also alias bashrc to quickly toggle to this venv witht the cmd `env-oscar` with location /home/pi/code/env-oscar
# Date Modified:  Wed Oct 14 15:36:50 IST 2020
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
cd ..
CWD=$(pwd)

##################### START YOUR CODE HERE ################### 
echo 'creating a venv called env-oscar ...'
#read
python3 -m venv $CWD/env-oscar
source $CWD/env-oscar/bin/activate
readonly sourceFile="$CWD/env-oscar/bin/activate"

echo 'adding alias env-oscar to ~/.bashrc'
echo  "alias env-oscar=source ${sourceFile}" >> ~/.bashrc
. ~/.bashrc
env-oscar
echo 'installing pip requirements in this venv'
#pip3 install -r requirements.txt


####################### END OF SCRIPT #######################

