/*
* Author: Param Deshpande
* Date created:  Sun 26 Apr 23:26:36 IST 2020
* Description: 
* For helper functions needed for the code to run regarding strings , arrays , general optimizations, basically helper functions which couldnt be cgorized into any other file.
* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------
*/
#include "main.h"
#include "commons.h"
#include "utils.h"


/*DEFINE YOUR GLOBAL VARS HERE*/

/*DEFINE YOUR PRIVATE VARS HERE*/


/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/


/* START YOUR CODE HERE */





void get_object_params(String message){
    char receivedChars[] = "motherfucking S capital Strings" ;
    int n = 0;
    while (message.charAt(n) != NULL){
        receivedChars[n] = message.charAt(n);
        ++n;
    }
    //  Assuming that now my string is equal to len of rec message.
    receivedChars[n] = '\0';
    for(int i =0; i<message.length(); i++){
        receivedChars[i] = message.charAt(i);
    }
    char * token; // this is used by strtok() as an index

    token = strtok(receivedChars,",");      // get the first part - the string
    object_area = atof(token);
    
    token = strtok(NULL, ",");
    object_cx = atof(token);
    
    token = strtok(NULL, ",");
    object_cy = atof(token);
    

}




/* END OF FILE */

