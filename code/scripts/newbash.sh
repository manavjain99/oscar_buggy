#!/bin/bash

# Author : Param Deshpande 
# Date Created : 7/07/2020
# Description : Template to create bash files.
# Date Modified : 7/07/2020

# Definging vars to be used in the script
current_date=`date`
working_dir=`pwd`

echo 
echo "Creates new .bash $working_dir file in this folder.."
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
touch $file_name.bash
chmod a+x $file_name.bash
################### ADDING CONTENT FOR .bash FILE ###################


# Add content like Author, date created, description, and date modified.
#echo >> $file_name
echo "#!/bin/bash" >> $file_name.bash
echo "" >> $file_name.bash
echo "# Author: Param Deshpande" >> $file_name.bash
echo "# Date Created: " $current_date  >> $file_name.bash
echo "# Description: "$description  >> $file_name.bash
echo "# Date Modified: " $current_date  >> $file_name.bash

echo '# License :
# ------------------------------------------------------------
# "THE BEERWARE LICENSE" (Revision 42):
# Param Deshpande wrote this code. As long as you retain this 
# notice, you can do whatever you want with this stuff. If we
# meet someday, and you think this stuff is worth it, you can
# buy me a beer in return.
# ------------------------------------------------------------' >> $file_name.bash
echo "#" >> $file_name.bash

echo "" >> $file_name.bash
echo "" >> $file_name.bash

echo "###################  DEFINE YOUR VARS HERE ###################" >> $file_name.bash
echo "" >> $file_name.bash
echo "" >> $file_name.bash

echo "##################### START YOUR CODE HERE ################### " >> $file_name.bash
echo "echo" >> $file_name.bash
echo "#echo" >> $file_name.bash
echo "#read" >> $file_name.bash

echo "" >> $file_name.bash
echo "" >> $file_name.bash
echo "" >> $file_name.bash
echo "" >> $file_name.bash
echo "" >> $file_name.bash

# Add end of script.
echo "####################### END OF SCRIPT #######################"  >> $file_name.bash
echo  "" >> $file_name.bash
# show th script.
#nano $file_name

read -p "Do you want to open the file ? [Y/n]" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[yY]$ ]]
then
    nano $file_name.bash
fi

read -p "Do you wish to execute the edited file ? [Y/n]" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[yY]$ ]]
then
    ./$file_name.bash
fi

echo

################### END OF SCRIPT ###################