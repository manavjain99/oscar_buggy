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

char last_command[100] = "";
bool python_command_flag = false;
bool newDataFromPC = false;

/*DEFINE YOUR PRIVATE VARS HERE*/
HardwareSerial uart_gimbal (PA12, PA11);

static const byte buffSize = 40;
static char inputBuffer[buffSize];
static const char startMarker = '<';
static const char endMarker = '>';
static byte bytesRecvd = 0;
static boolean readInProgress = false;


/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/
static void parseData();


/* START YOUR CODE HERE */


void init_uart(void){
    uart_obcomp.begin(115200);
    //uart_dbugcon.begin(9600);
    uart_gimbal.begin(115200);   
}


// I am so far getting only gimbal delta roll,pitch,yaw.


void parse_data() {

    // split the data into its parts
    
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(inputBuffer,",");      // get the first part - the string
  object_area = atoi(strtokIndx);
    
  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  object_cx = atoi(strtokIndx);     // convert this part to an integer
  
  strtokIndx = strtok(NULL, ","); 
  object_cy = atoi(strtokIndx);     // convert this part to a float

}


// See references for this code. ArduinoPC2.ino
void rcv_obcomp(void){

    // receive data from PC and save it into inputBuffer
    
  while(uart_obcomp.available()) {

    char x = uart_obcomp.read();

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
      parse_data();
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
    uart_obcomp.print(ACK_REC_PARAMS);
  }   
}

void send_until_ack(void){
    while(1){
        uart_obcomp.print(ACK_REC_PARAMS);

    }
}


void rcv_ack_params(void){
    rcv_obcomp();
    ack_obcomp();
}


/* END OF FILE */

