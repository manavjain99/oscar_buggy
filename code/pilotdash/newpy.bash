#!/bin/bash

# Author : Param Deshpande 
# Date Created : 23/04/2020
# Description : Creates formatted cpp and header files.
# Date Modified : 23/04/2020

# Definging vars to be used in the script
current_date=`date`

echo 
echo "Creates new python file with all comments and stuff."
echo 

# Get file name from the user.
echo "Enter the file name without any extension."
#echo
read file_name
echo

echo "Enter description for the file."
#echo
read description
echo
# create that file 
touch $file_name.py
################### ADDING CONTENT FOR .py FILE ###################

# Add content like Author, date created, description, and date modified.
#echo >> $file_name
#echo "# This file was autocreated by GENIUSES" >> $file_name
echo '"""' >> $file_name.py
#echo "" >>$file_name.py
echo " Author: Param Deshpande" >>$file_name.py
echo " Date created: " $current_date  >>$file_name.py
echo " Description: " >>$file_name.py
echo " "$description >> $file_name.py

echo ' License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------' >>$file_name.py
echo " date modified: " $current_date >> $file_name.py
#echo "" >>$file_name.py
echo '"""' >>$file_name.py

echo '' >>$file_name.py

echo '#import ' >>$file_name.py
echo '#import ' >>$file_name.py

echo '' >>$file_name.py

echo "#if __name__ == '__main__':">>$file_name.py
echo '  #import ' >>$file_name.py
echo '  #import ' >>$file_name.py

echo '' >>$file_name.py

echo '""" WRITE YOUR FUNCTIONS HERE """' >>$file_name.py

# Making 3 functions.

echo '' >>$file_name.py
echo "#def ...:" >>$file_name.py
echo '#  """' >>$file_name.py
echo '#  () -> ()' >>$file_name.py
echo '#  Description: ' >>$file_name.py
echo '#  >>>' >>$file_name.py
echo '#  ' >>$file_name.py
echo '#  """' >>$file_name.py
echo '' >>$file_name.py


echo '' >>$file_name.py
echo "#def ...:" >>$file_name.py
echo '#  """' >>$file_name.py
echo '#  () -> ()' >>$file_name.py
echo '#  Description: ' >>$file_name.py
echo '#  >>>' >>$file_name.py
echo '#  ' >>$file_name.py
echo '#  """' >>$file_name.py
echo '' >>$file_name.py


echo '' >>$file_name.py
echo "#def ...:" >>$file_name.py
echo '#  """' >>$file_name.py
echo '#  () -> ()' >>$file_name.py
echo '#  Description: ' >>$file_name.py
echo '#  >>>' >>$file_name.py
echo '#  ' >>$file_name.py
echo '#  """' >>$file_name.py
echo '' >>$file_name.py


echo '""" START YOUR CODE HERE """' >>$file_name.py
echo '' >>$file_name.py
echo "if __name__ == '__main__':" >>$file_name.py
echo "  pass" >>$file_name.py
echo "  #import doctest" >>$file_name.py
echo "  #doctest.testmod()" >>$file_name.py
echo "  " >>$file_name.py
echo "  " >>$file_name.py
echo "  " >>$file_name.py
echo "  " >>$file_name.py

# Add end of script.
echo '""" END OF FILE """' >>$file_name.py
echo  "" >>$file_name.py
# show th script.
#nano $file_name
# End of this script.
echo Python file created successfully.

echo
echo End of script.
echo


