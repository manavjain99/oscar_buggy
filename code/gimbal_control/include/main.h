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
#ifndef main_h
#define main_h

#include <Arduino.h>
#include <cmath>
#include <string> // for string and to_string() 

/*GLOBAL DEFS*/ 
#define TICK_DURATION_MS (300.0)
#define UART_DEBUG

/* EXTERN YOUR GLOBAL VARS HERE*/

extern float object_area;
extern float object_cx  ; 
extern float object_cy  ;

extern float frame_ht ;
extern float frame_wd ;

extern float new_msg_time_MS;


/* DEFINE YOUR GLOBAL FUNCTION OR TASKS PROTOTYPES HERE*/

//void 
//void 

#endif


/* END OF FILE */

