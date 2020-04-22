/*
    Testing for comms betn python to stm via UART.

    UART data sent via python via TTL to UART port 1 of stm ie Serial1 (PA12, PA11);
    stm comms back to PC via uart2 ie Serial2 (PINS D1,D0).

*/

#include <Arduino.h>

#define to_PC Serial2 
#define from_PYTHON Serial1

String python_message = "";

HardwareSerial from_PYTHON (PA12, PA11);

void setup(){
    to_PC.begin(9600);
    from_PYTHON.begin(9600);
    //to_GIMBAL.begin(230400); /*DURING FIRMWARE UPGRADE OF GIMBAL SWITCH TO THIS FREQ*/
    //to_GIMBAL.setTx(PA11);
    //to_GIMBAL.setRx(PA12);
    pinMode(LED_BUILTIN, OUTPUT);
   
    //to_GIMBAL.print("can you see me ?");
    
  }


  void loop(){   
      // send data only when you receive data:
  from_PYTHON.println("Hey python can you see me.");
  if (from_PYTHON.available() > 0) {
    // Read python message.
    python_message = from_PYTHON.readString();  

    // say what you got:
    from_PYTHON.println("In the python console I should get");
    from_PYTHON.println(python_message);
    to_PC.print("I received from python: ");
    to_PC.println(python_message);

  }
}
