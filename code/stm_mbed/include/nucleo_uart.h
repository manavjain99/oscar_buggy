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
#ifndef nucleo_uart_h
#define nucleo_uart_h

/* EXTERN YOUR GLOBAL VARS HERE*/
//#define uart_gimbal Serial1
//#define uart_obcomp Serial2
#include "../mbed-os/mbed.h"

const char ACK_REC_PARAMS[] =  "<1>";
const char ACK_STM[]        =  "<STM_ACK>";
const char STM_READY[]      =  "<STM_READY>";

extern BufferedSerial uart_obcomp;
extern BufferedSerial uart_debugcon;
extern BufferedSerial uart_gimbal ;

extern bool newDataFromPC;

//extern 
//extern 


/* DEFINE YOUR GLOBAL FUNCTION OR TASKS PROTOTYPES HERE*/

void init_uart();
//void rcv_parse_obcomp(void);
void ack_obcomp(void);
//void getDataFromPC();
void rcv_obcomp(void);
void parse_data(void);
//void send_until_ack(String, String );
/*send_message, ack_message*/
void rcv_ack_params(void);


#endif


/* END OF FILE */

