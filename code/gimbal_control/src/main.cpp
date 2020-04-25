/*
* Author: Param Deshpande
* Date created:  Sat 25 Apr 19:21:45 IST 2020
* Description: 
* Main file for the stm32 MCU responsilble for controlling the gimbal and the buggy.
* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------
*/
#include "../include/main.h"
#include "../include/commons.h"
#include "../include/uart.hpp"


/*DEFINE YOUR GLOBAL VARS HERE*/


/*DEFINE YOUR PRIVATE VARS HERE*/


/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/


/* START YOUR CODE HERE */
void setup(void){
    init_uart();
    
}

void loop(){
    send_until_ack("STM_READY", "ACK");
    rec_and_ack("REC");
}


/* END OF FILE */

