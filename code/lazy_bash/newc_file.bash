#!/bin/bash

# Author : Param Deshpande 
# Date Created : 23/04/2020
# Description : A template for making c and cpp files.
# Date Modified : 23/04/2020

# Definging vars to be used in the script
current_date=`date`

echo 
echo "I am writing a bash scipt to write a cpp script ain't that rad."
#echo 

# Get file name from the user.
echo hey budddy enter the file name.
read file_name
echo
# create that file 
touch $file_name

# Make it executable.
#chmod a+x $file_name

# Make it a bash script.
#echo "#!/bin/bash" >> $file_name

# Add content like Author, date created, description, and date modified.
#echo >> $file_name
#echo "# This file was autocreated by GENIUSES" >> $file_name
echo "/*" >> $file_name
echo "* Author: Param Deshpande" >> $file_name
echo "* Date created: " $current_date  >> $file_name
echo "* Description: " >> $file_name
echo '* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------' >> $file_name
echo "*/" >> $file_name

echo "#include<main.h>" >> $file_name
echo "#include<commons.h>" >> $file_name
echo "#include<"$file_name".h>" >> $file_name

echo "" >> $file_name
echo "" >> $file_name

echo "/*DEFINE YOUR GLOBAL VARS HERE*/" >> $file_name
echo "" >> $file_name
echo "" >> $file_name

echo "/*DEFINE YOUR PRIVATE VARS HERE*/" >> $file_name
echo "" >> $file_name
echo "" >> $file_name

echo "/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/" >> $file_name
echo "" >> $file_name
echo "" >> $file_name

echo "/* START YOUR CODE HERE */" >> $file_name
echo "" >> $file_name
echo "" >> $file_name
echo "" >> $file_name
echo "" >> $file_name
echo "" >> $file_name

# Add end of script.
echo "/* END OF FILE */"  >> $file_name
echo  "" >> $file_name
# show th script.
#nano $file_name

# End of this script.
echo file Created successfully.
echo End of script.
echo


