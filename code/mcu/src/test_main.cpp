//#define PYTHON_UART
#ifdef PYTHON_UART
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

#endif

#ifdef GIMBALC
#include <Arduino.h>

  #include "../mavlink/include/mavlink_types.h"
  #include "../mavlink/include/mavlink.h"
  #include "../mavlink/include/mavlink.h"


  #define ToDeg(x) (x*57.2957795131)  // *180/pi
  #define to_PC Serial2 
  #define to_GIMBAL Serial1
  #define INCREASING HIGH
  #define DECREASING LOW
  
  //#define MODIFIED

  #ifdef MODIFIED
  HardwareSerial Serial2 (PA11, PA12);
  #endif 

  union byteToFloat
  {
      struct
      {
        byte b0 :8;
        byte b1 :8;
        byte b2 :8;
        byte b3 :8;
      } bytes;
      float f;
  };

  union byteToInt
  {
      struct
      {
        byte b0 :8;
        byte b1 :8;
      } bytes;
      uint16_t i;
  };

  union intFloat
  {
      int i;
      float f;
  };



  void read_mavlink_storm32(){ 
    
    mavlink_message_t msg;
    mavlink_status_t status;
    
    while (to_GIMBAL.available() > 0) {
      
      uint8_t c = to_GIMBAL.read();
      //trying to grab msg
      if (mavlink_parse_char(MAVLINK_COMM_0, c, &msg, &status)) {   
        switch (msg.msgid) {
          case MAVLINK_MSG_ID_ATTITUDE:
            {
              //get pitch and yaw angle from storm (requestAttitude() must be executed first)
              double gimbalYaw = ToDeg(mavlink_msg_attitude_get_yaw(&msg));
              double gimbalPitch = ToDeg(mavlink_msg_attitude_get_pitch(&msg));
            }
            break;
            
          case MAVLINK_MSG_ID_PARAM_VALUE:
            {
              //get parameter value from storm (parameter 66 is pan mode, requestParameter(int id) must be executed first)
              if(mavlink_msg_param_value_get_param_index(&msg) == 66)
                int panMode = mavlink_msg_param_value_get_param_value(&msg);
            }
            break;
          default:
            break;
        }
      }  
    }
    
  }

  void requestAttitude(){

    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 1234, 0, 0, 0, 0, 0, 0, 0, 0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    to_GIMBAL.write(buf, len);
  
  }

  void requestParameter(int id){
      
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_param_request_read_pack(255, 1, &msg, 71, 67, "", id);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    to_GIMBAL.write(buf, len);   
    
  }

  void setParameter(int id, int val){

      intFloat parameterValue;
      parameterValue.i = val;
      
      mavlink_message_t msg;
      uint8_t buf[MAVLINK_MAX_PACKET_LEN];
      mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 180, 0, id, parameterValue.f, 0.0, 0.0, 0.0, 0.0, 0.0);
      uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
      to_GIMBAL.write(buf, len); 
        
  }


  void setAngles(float roll, float pitch, float yaw){
    
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 205, 0, pitch, roll, yaw, 0.0, 0.0, 0.0, 0.0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    to_GIMBAL.write(buf, len);
    
  }

  void recenter(){
    
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 204, 0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    to_GIMBAL.write(buf, len);
    
  }

  void setRc(byte type, uint16_t val){
    
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];

    byteToInt tmpVal;
    tmpVal.i = val; 
    
    byteToFloat data1;
    data1.bytes.b0 = 0xFA;
    data1.bytes.b1 = 0x02;
    data1.bytes.b2 = type;
    data1.bytes.b3 = tmpVal.bytes.b0;

    byteToFloat data2;
    data2.bytes.b0 = tmpVal.bytes.b1;
    data2.bytes.b1 = 0;
    data2.bytes.b2 = 0;
    data2.bytes.b3 = 0;
    
    mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 1235, 0, data1.f, data2.f, 0.0, 0.0, 0.0, 0.0, 0.0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    to_GIMBAL.write(buf, len);  
  }



  void setRcPitch(uint16_t val){
    setRc(0x0A, val);
  }

  void setRcRoll(uint16_t val){
    setRc(0x0B, val);
  }

  void setRcYaw(uint16_t val){
    setRc(0x0C, val);
  }

  HardwareSerial to_GIMBAL (PA12, PA11);

  void setup(){
    to_PC.begin(9600);
    to_GIMBAL.begin(115200);
    //to_GIMBAL.begin(230400); /*DURING FIRMWARE UPGRADE OF GIMBAL SWITCH TO THIS FREQ*/
    //to_GIMBAL.setTx(PA11);
    //to_GIMBAL.setRx(PA12);
    pinMode(LED_BUILTIN, OUTPUT);
   
    //to_GIMBAL.print("can you see me ?");
    
  }

  bool state = LOW;
  int test_angle = 0;
  bool angle_status = INCREASING;

  void loop(){   
    digitalWrite(LED_BUILTIN, state);
    //to_GIMBAL.print("can you see me ? Serial 1 ");
    to_PC.println("can you see me ? Serial ");
    if ((angle_status == INCREASING)  )
    {
      test_angle++;
      if(test_angle > 25){
       (angle_status = DECREASING);
      }
    }
    else if (angle_status == DECREASING )
    {
      test_angle--;
      if(test_angle < 0){
       (angle_status = INCREASING);
      }
    }
    setAngles(test_angle,test_angle,test_angle);
    state = !state;
    delay(50);
    
    //read_mavlink_storm32();
    
  }
#endif