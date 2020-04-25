#include <Arduino.h>

#define to_PC Serial2 
#define from_PYTHON Serial1

String python_message = "";

HardwareSerial from_PYTHON (PA12, PA11);

void setup(){
    to_PC.begin(9600);
    from_PYTHON.begin(115200);
    //to_GIMBAL.begin(230400); /*DURING FIRMWARE UPGRADE OF GIMBAL SWITCH TO THIS FREQ*/
    //to_GIMBAL.setTx(PA11);
    //to_GIMBAL.setRx(PA12);
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    
    //to_GIMBAL.print("can you see me ?");
    
  }

  String send_message = "STM_READY";
  String ACK_STR = "ACK";
  void loop(){   
    if (from_PYTHON.available() > 0) {
    // Read python message.
      python_message = from_PYTHON.readStringUntil('\n');
      //send_message = from_PYTHON.available();
      send_message = python_message;
      
      if(python_message.equals("99\r")){
      digitalWrite(LED_BUILTIN, LOW);
      send_message = "LED SHOULD BE";
      
      }

      // say what you got:
      //from_PYTHON.println("In the python console I should get");
      //from_PYTHON.println(python_message);
      //to_PC.print("I received from python: ");
      //to_PC.println(python_message);

  }
}
