#!/bin/bash

# Author : Param Deshpande 
# Date Created : 23/04/2020
# Description : Creates formatted cpp and header files.
# Date Modified : 23/04/2020

# Definging vars to be used in the script
current_date=`date`

echo 
echo "Creates new cpp and header file in /src and /include."
echo 

# Get file name from the user.
echo "Enter the file name without any extension."
#echo
read file_name
echo

echo "Enter description for the files."
#echo
read description
echo
# create that file 
touch src/$file_name.cpp
touch include/$file_name.h

################### ADDING CONTENT FOR .cpp FILE ###################

# Add content like Author, date created, description, and date modified.
#echo >> $file_name
#echo "# This file was autocreated by GENIUSES" >> $file_name
echo "/*" >>src/$file_name.cpp
echo "* Author: Param Deshpande" >>src/$file_name.cpp
echo "* Date created: " $current_date  >>src/$file_name.cpp
echo "* Description: " >>src/$file_name.cpp
echo "* "$description >> src/$file_name.cpp

echo '* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------' >>src/$file_name.cpp
echo "*/" >>src/$file_name.cpp

echo '#include "main.h"' >>src/$file_name.cpp
echo '#include "commons.h"' >>src/$file_name.cpp
echo '#include "'$file_name'.h"' >>src/$file_name.cpp

echo "" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp

echo "/*DEFINE YOUR GLOBAL VARS HERE*/" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp

echo "/*DEFINE YOUR PRIVATE VARS HERE*/" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp

echo "/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp

echo "/* START YOUR CODE HERE */" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp
echo "" >>src/$file_name.cpp

# Add end of script.
echo "/* END OF FILE */"  >>src/$file_name.cpp
echo  "" >>src/$file_name.cpp
# show th script.
#nano $file_name



################### ADDING CONTENT FOR .h FILE ###################

echo "/*" >> include/$file_name.h
echo "* Author: Param Deshpande" >> include/$file_name.h
echo "* Date created: " $current_date  >> include/$file_name.h
echo "* Description: " >> include/$file_name.h
echo "* "$description >> include/$file_name.h

echo '* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------' >> include/$file_name.h
echo "*/" >> include/$file_name.h


echo "#ifndef "$file_name"_h" >> include/$file_name.h
echo "#define "$file_name"_h" >> include/$file_name.h

echo "" >> include/$file_name.h
echo "" >> include/$file_name.h

echo "/* EXTERN YOUR GLOBAL VARS HERE*/" >> include/$file_name.h
echo "" >> include/$file_name.h

echo "//extern " >> include/$file_name.h
echo "//extern " >> include/$file_name.h

echo "" >> include/$file_name.h
echo "" >> include/$file_name.h

echo "/* DEFINE YOUR GLOBAL FUNCTION OR TASKS PROTOTYPES HERE*/" >> include/$file_name.h
echo "" >> include/$file_name.h

echo "//void " >> include/$file_name.h
echo "//void " >> include/$file_name.h
echo "" >> include/$file_name.h
echo "#endif" >> include/$file_name.h
echo "" >> include/$file_name.h
echo "" >> include/$file_name.h

# Add end of script.
echo "/* END OF FILE */"  >> include/$file_name.h
echo  "" >> include/$file_name.h
# show th script.
#nano $file_name

# End of this script.
echo cpp header pair Created successfully.

echo
echo End of script.
echo


