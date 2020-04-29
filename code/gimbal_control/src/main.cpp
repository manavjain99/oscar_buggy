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
#include "../include/main.h" 

void setup(){

}

void loop(){

}
#endif

#ifndef DEBUG
#include "../include/main.h"
#include "../include/commons.h"
#include "../include/uart.hpp"
#include "../include/utils.h"
#include "gimbal_stuff.h"
/*DEFINE YOUR GLOBAL VARS HERE*/
float frame_ht = -1.0F;
float frame_wd = -1.0F;

float object_area = -1.0F;
float object_cx   = -1.0F;
float object_cy   = -1.0F;

/*DEFINE YOUR PRIVATE VARS HERE*/


/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/


/* START YOUR CODE HERE */
void setup(void){
    init_uart();
    init_gimbal();
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    
}
String object_area_String = " ";
        
void loop(){
    /*SEND READY */
    send_until_ack("STM_READY", "ACK");
    //
    // Get frame size.
    String str_frame_ht = rec_and_ack("ACK_FH");
    frame_ht = str_frame_ht.toFloat();
    
    String str_frame_wd = rec_and_ack("ACK_FW");
    frame_wd = str_frame_wd.toFloat();
    
    
    String object_center = "HI";
    while(1){
        // Get data of object center coords.
        object_center = rec_and_ack("ACK_OC");
        get_object_params(object_center);
        //get_pix_per_deg();         
        if(object_area == float(100)){
            //digitalWrite(LED_BUILTIN, LOW);
            orient_gimbal();
        }

        else{
            digitalWrite(LED_BUILTIN, HIGH);
        }
        //object_area_String = String(object_area, 7);
        
     // Put PID LOOP for angles.
     // Done with gimbal control for obj detection.
    
    }

}

#endif

/* END OF FILE */

