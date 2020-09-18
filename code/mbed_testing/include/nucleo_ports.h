/*
* Author: Param Deshpande
* Date created:  Sat 25 Apr 17:20:37 IST 2020
* Description: 
* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------
*/
#ifndef nucleo_ports_h
#define nucleo_ports_h

#include "../mbed-os/mbed.h"

/*GLOBAL DEFS*/ 
#define nucleo_rx_stlink_pin PA_10
#define nucleo_tx_stlink_pin PA_9

#define nucleo_rx_gimbal_pin PA_12
#define nucleo_tx_gimbal_pin PA_11

#define nucleo_rx_obcomp_pin PA_2
#define nucleo_tx_obcomp_pin PA_3

#define on_board_led LED1
/* EXTERN YOUR GLOBAL VARS HERE*/

#endif


/* END OF FILE */

