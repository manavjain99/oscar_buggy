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
//#define DEBUG
#ifdef DEBUG 



#endif

#ifndef DEBUG
#include "../include/main.h"
#include "../include/commons.h"
#include "../include/uart.hpp"

/*DEFINE YOUR GLOBAL VARS HERE*/


/*DEFINE YOUR PRIVATE VARS HERE*/


/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/


/* START YOUR CODE HERE */
void setup(void){
    init_uart();
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    
}

void loop(){
    /*SEND READY */
    send_until_ack("STM_READY", "ACK");
    //
    // Get frame size.
    String str_frame_ht = rec_and_ack("ACK_FH");
    float frame_ht = str_frame_ht.toFloat();
    String str_frame_wd = rec_and_ack("ACK_FW");
    float frame_wd = str_frame_wd.toFloat();
    digitalWrite(LED_BUILTIN, LOW);
    
    String object_center = "HI";
    while(1){
        // Get data of object center coords.
        digitalWrite(LED_BUILTIN, HIGH);
        object_center = rec_and_ack("ACK_OC");
        digitalWrite(LED_BUILTIN, LOW);
        object_center = " ";
        // Put PID LOOP for angles.

        // Done with gimbal control for obj detection.
    }

}

#endif

/* END OF FILE */

