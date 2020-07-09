#!/bin/bash

# Author : Param Deshpande 
# Date Created : 23/04/2020
# Description : Creates formatted cpp and header files.
# Date Modified : 23/04/2020

# Definging vars to be used in the script
current_date=`date`

echo 
echo "I am writing a bash scipt to write a cpp script ain't that rad."
#echo 

# Get file name from the user.
echo hey budddy enter the file name without the extension.
read file_name
echo
# create that file 
touch $file_name.cpp
touch $file_name.h

################### ADDING CONTENT FOR .cpp FILE ###################

# Add content like Author, date created, description, and date modified.
#echo >> $file_name
#echo "# This file was autocreated by GENIUSES" >> $file_name
echo "/*" >> $file_name.cpp
echo "* Author: Param Deshpande" >> $file_name.cpp
echo "* Date created: " $current_date  >> $file_name.cpp
echo "* Description: " >> $file_name.cpp
echo '* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------' >> $file_name.cpp
echo "*/" >> $file_name.cpp

echo '#include "main.h"' >> $file_name.cpp
echo '#include "commons.h"' >> $file_name.cpp
echo '#include "'$file_name'.h"' >> $file_name.cpp

echo "" >> $file_name.cpp
echo "" >> $file_name.cpp

echo "/*DEFINE YOUR GLOBAL VARS HERE*/" >> $file_name.cpp
echo "" >> $file_name.cpp
echo "" >> $file_name.cpp

echo "/*DEFINE YOUR PRIVATE VARS HERE*/" >> $file_name.cpp
echo "" >> $file_name.cpp
echo "" >> $file_name.cpp

echo "/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/" >> $file_name.cpp
echo "" >> $file_name.cpp
echo "" >> $file_name.cpp

echo "/* START YOUR CODE HERE */" >> $file_name.cpp
echo "" >> $file_name.cpp
echo "" >> $file_name.cpp
echo "" >> $file_name.cpp
echo "" >> $file_name.cpp
echo "" >> $file_name.cpp

# Add end of script.
echo "/* END OF FILE */"  >> $file_name.cpp
echo  "" >> $file_name.cpp
# show th script.
#nano $file_name



################### ADDING CONTENT FOR .h FILE ###################

echo "/*" >> $file_name.h
echo "* Author: Param Deshpande" >> $file_name.h
echo "* Date created: " $current_date  >> $file_name.h
echo "* Description: " >> $file_name.h
echo '* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------' >> $file_name.h
echo "*/" >> $file_name.h


echo "#ifndef<"$file_name".h>" >> $file_name.h
echo "#define<"$file_name".h>" >> $file_name.h

echo "" >> $file_name.h
echo "" >> $file_name.h

echo "/* EXTERN YOUR GLOBAL VARS HERE*/" >> $file_name.h
echo "" >> $file_name.h

echo "//extern " >> $file_name.h
echo "//extern " >> $file_name.h

echo "" >> $file_name.h
echo "" >> $file_name.h

echo "/* DEFINE YOUR GLOBAL FUNCTION OR TASKS PROTOTYPES HERE*/" >> $file_name.h
echo "" >> $file_name.h

echo "//void " >> $file_name.h
echo "//void " >> $file_name.h
echo "" >> $file_name.h
echo "#endif" >> $file_name.h
echo "" >> $file_name.h
echo "" >> $file_name.h

# Add end of script.
echo "/* END OF FILE */"  >> $file_name.h
echo  "" >> $file_name.h
# show th script.
#nano $file_name

# End of this script.
echo cpp header pair Created successfully.

echo
echo End of script.
echo


