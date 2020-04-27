/*
* Author: Param Deshpande
* Date created:  Sat 25 Apr 19:24:57 IST 2020
* Description: 
* Takes care of the UART needed for gimbal, obcomp and debug_console.
* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------
*/
#ifndef uart_hpp
#define uart_hpp

#include "main.h"
#include "Arduino.h"
#include "string.h"
/* EXTERN YOUR GLOBAL VARS HERE*/
#define uart_gimbal Serial1
#define uart_obcomp Serial2
//#define uart_dbugcon Serial3 

extern HardwareSerial uart_obcomp;
//extern HardwareSerial uart_dbugcon;
extern HardwareSerial uart_gimbal ;

//extern 
//extern 


/* DEFINE YOUR GLOBAL FUNCTION OR TASKS PROTOTYPES HERE*/

void init_uart();
void send_until_ack(String, String );
/*send_message, ack_message*/
String rec_and_ack(String);


#endif


/* END OF FILE */

