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


#include "../include/commons.h"
#include "../include/nucleo_uart.h"
#include "include/nucleo_ports.h"
#include "../include/gimbal_stuff.h"

/*DEFINE YOUR GLOBAL VARS HERE*/

char last_command[500] = "";
bool newDataFromPC = false;

/*DEFINE YOUR PRIVATE VARS HERE*/
BufferedSerial uart_gimbal (nucleo_rx_gimbal_pin, nucleo_tx_gimbal_pin);  //Board RX, TX
BufferedSerial uart_debugcon (nucleo_rx_stlink_pin, nucleo_tx_stlink_pin);  //Board RX, TX
BufferedSerial uart_obcomp(nucleo_rx_obcomp_pin, nucleo_rx_obcomp_pin);

static const uint16_t buffSize = 500;
static char inputBuffer[buffSize];
static const char startMarker = '<';
static const char endMarker = '>';
static byte bytesRecvd = 0;
static bool readInProgress = false;

#define MAXIMUM_BUFFER_SIZE                                                  128

char buf[MAXIMUM_BUFFER_SIZE] = {0};



float object_area;
float object_cx  ; 
float object_cy  ;

float frame_ht ;
float frame_wd ;





/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/
static void parseData();


/* START YOUR CODE HERE */


void init_uart(void){
    uart_obcomp.set_baud(115200);
    uart_debugcon.set_baud(115200);
    uart_gimbal.set_baud(115200);   

    uart_obcomp.set_format(
        /* bits */ 8,
        /* parity */ BufferedSerial::None,
        /* stop bit */ 1
    );
    uart_debugcon.set_format(
        /* bits */ 8,
        /* parity */ BufferedSerial::None,
        /* stop bit */ 1
    );
    uart_gimbal.set_format(
        /* bits */ 8,
        /* parity */ BufferedSerial::None,
        /* stop bit */ 1
    );

}


void parse_data_params() {

    // split the data into its parts
    
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(inputBuffer,",");      // get the first part - the string
  object_area = atoi(strtokIndx);
    
  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  object_cx = atoi(strtokIndx);     // convert this part to an integer
  
  strtokIndx = strtok(NULL, ","); 
  object_cy = atoi(strtokIndx);     // convert this part to a float

}

/**
 * Parses 4 coeffs for imgx ie yaw and 4coeffs for imgy ie pitch
 * Global inputBuffer = "1,2,3,4,5,..." receivd by rcv_obcomp
*/
void parse_data_coeffs(void){

   // split the data into its parts
    
  char * strtokIndx; // this is used by strtok() as an index
  
  // Coeff2
  strtokIndx = strtok(inputBuffer,",");      // get the first part - the string
  a2x = atof(strtokIndx);

  strtokIndx = strtok(NULL, ","); 
  b2x = atof(strtokIndx);   
  
  strtokIndx = strtok(NULL, ","); 
  c2x = atof(strtokIndx);   

  strtokIndx = strtok(NULL, ","); 
  d2x = atof(strtokIndx);   

  // Coeff3
  strtokIndx = strtok(NULL, ","); 
  a3x = atof(strtokIndx);   
  
  strtokIndx = strtok(NULL, ","); 
  b3x = atof(strtokIndx);   
  
  strtokIndx = strtok(NULL, ","); 
  c3x = atof(strtokIndx);   

  strtokIndx = strtok(NULL, ","); 
  d3x = atof(strtokIndx);   

  // Coeff4 
  strtokIndx = strtok(NULL, ","); 
  a4x = atof(strtokIndx);   
  
  strtokIndx = strtok(NULL, ","); 
  b4x = atof(strtokIndx);   
  
  strtokIndx = strtok(NULL, ","); 
  c4x = atof(strtokIndx);   

  strtokIndx = strtok(NULL, ","); 
  d4x = atof(strtokIndx);   
}

// See references for this code. ArduinoPC2.ino
void rcv_obcomp(void){

    // receive data from PC and save it into inputBuffer
    
  while(uart_obcomp.readable()) {

    char x = uart_obcomp.read(buf, sizeof(buf));

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      for (int i = 0; i < bytesRecvd -1 ; i++){
      last_command[i] = inputBuffer[i];
      }
      //Completing the string.
      last_command[bytesRecvd] = '\0';
      inputBuffer[bytesRecvd] = 0;
      parse_data_coeffs();
     }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1; 
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}
void ack_obcomp(void){
 
  if (newDataFromPC) {
    newDataFromPC = false;
    uart_obcomp.write(ACK_REC_PARAMS, sizeof(ACK_REC_PARAMS));
  }   
}

void send_until_ack(void){
    while(1){
        uart_obcomp.write(ACK_REC_PARAMS,sizeof(ACK_REC_PARAMS));

    }
}


void rcv_ack_params(void){
    rcv_obcomp();
    ack_obcomp();
}


/* END OF FILE */

