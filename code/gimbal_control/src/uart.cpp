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


#include "../include/main.h"
#include "../include/commons.h"
#include "../include/uart.hpp"


/*DEFINE YOUR GLOBAL VARS HERE*/

#define uart_obcomp Serial1
#define uart_dbugcon Serial2 


/*DEFINE YOUR PRIVATE VARS HERE*/

HardwareSerial uart_obcomp (PA12, PA11);


/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/


/* START YOUR CODE HERE */

String python_message = "";

void init_uart(void){
    uart_obcomp.begin(115200);
    uart_dbugcon.begin(9600);
    
}

void send_until_ack(String send_message, String ack_message){
    /*Sends a packet of data until acknowledge by the onborad comp ie obcomp*/
    while (1){
        uart_obcomp.println(send_message);
        uart_dbugcon.println("Send until ack by STM32");
        /*If ack data sent by obcomp*/
        if(uart_obcomp.available() > 0){
            String rec_message = uart_obcomp.readStringUntil('\n');
            
            if(rec_message.equals(ack_message+"\r")){
                break;
            }
        }
    }
}

String rec_and_ack(String ack_message){
    /*Receive and acknowledge. Dont fuck around, Please.*/
    while (1){
        /* code */
        if(uart_obcomp.available() > 0){
            String rec_message = uart_obcomp.readStringUntil('\n');
            
            // Removes last two chars ie '\r' 
            int str_len = rec_message.length();
            String is_backslash_r = rec_message.substring(str_len - 1);
            if(is_backslash_r.equals("\r")){
                rec_message = rec_message.substring(0, str_len - 1); 
            }
            return rec_message;
        }    
    }
    
}

  //String send_message = "STM_READY";
  //String ACK_STR = "ACK";
  //void loop(){   
//
  //  uart_obcomp.println(send_message);
  //  if (uart_obcomp.available() > 0) {
  //  // Read python message.
  //    python_message = uart_obcomp.readStringUntil('\n');
  //    //send_message = uart_obcomp.available();
  //    send_message = python_message;
  //    
  //    if(python_message.equals("ACK\r")){
  //    digitalWrite(LED_BUILTIN, LOW);
  //    send_message = "LED SHOULD BE";
  //    
  //    }
//
      // say what you got:
      //uart_obcomp.println("In the python console I should get");
      //uart_obcomp.println(python_message);
      //uart_dbugcon.print("I received from python: ");
      //uart_dbugcon.println(python_message);

//  }
//}//










/* END OF FILE */

