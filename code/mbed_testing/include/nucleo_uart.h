
#ifndef nucleo_uart_h
#define nucleo_uart_h

/* EXTERN YOUR GLOBAL VARS HERE*/
//#define uart_gimbal Serial1
//#define uart_obcomp Serial2
#include "../mbed-os/mbed.h"


//extern  BufferedSerial serial_port;
//extern  BufferedSerial uart_gimbal ;
//extern  BufferedSerial uart_obcomp ;
extern  BufferedSerial uart_debugcon;

void init_uart( BufferedSerial& );
/* DEFINE YOUR GLOBAL FUNCTION OR TASKS PROTOTYPES HERE*/

#endif

