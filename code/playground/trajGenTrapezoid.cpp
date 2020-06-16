/*
https://books.google.co.in/books?id=FiX1ceRT5zoC&pg=PR10&lpg=PR10&dq=trapezoidal+trajectory+cpp&source=bl&ots=KT877eTx4S&sig=ACfU3U35ceOVZ5l_Uv_xEPo_HqejJdg9zw&hl=en&sa=X&ved=2ahUKEwiPyK6gkcPpAhV67HMBHe78ATYQ6AEwB3oECAsQAQ#v=onepage&q=trapezoidal%20trajectory%20cpp&f=false
see eqns on pg 19 and 20 for acc,vel,dist a,b ie from 0 to flex pt and to destn pt.


*/
#include <iostream>
#include <string.h>
#include <stdlib.h>
/*
@brief: add these vals delta gimbal angles.
@inputs: object center coords.
eg. 
trajDeltaAngs = [[], [], [] ....]
trajGenTrapezoid( 239, 123 )
gimbalAng += 
*/


static const uint8_t buffSize = 200;
static char inputBuffer[buffSize];
static const char startMarker = '<';
static const char endMarker = '>';
static int8_t bytesRecvd = 0;
static bool readInProgress = false;

int object_area = 0;
int object_cx = 0;
float object_cy = 0;

void parse_data_params() {

    // split the data into its parts
    
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(inputBuffer,",");      // get the first part - the string
  object_area = atoi(strtokIndx);
    
  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  object_cx = atoi(strtokIndx);     // convert this part to an integer
  
  strtokIndx = strtok(NULL, ","); 
  object_cy = atof(strtokIndx);     // convert this part to a float

}

int main(){
    
    std::string recStr = "40,3,2.98";
    int i=0;
    for(char ch :recStr){
        inputBuffer[i++] = ch;
    }
    parse_data_params();
    std::cout << "object_area is " << object_area << " cx is " << object_cx << " cx is " << object_cy << std::endl;
    return 0;
}