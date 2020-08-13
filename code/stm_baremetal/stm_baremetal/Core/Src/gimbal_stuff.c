/*
 * gimbal_stuff.c
 *
 *  Created on: Aug 13, 2020
 *      Author: Param Deshpande
 */


#include "../Inc/main.h"
#include "../Inc/global.h"
#include "../Inc/gimbal_stuff.h"

#define uart_gimbal huart6


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


  void requestAttitude(){

    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 1234, 0, 0, 0, 0, 0, 0, 0, 0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    HAL_UART_Transmit(&uart_gimbal, (uint8_t*)buf, len, 100);


  }


  void requestParameter(int id){
      
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_param_request_read_pack(255, 1, &msg, 71, 67, "", id);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    HAL_UART_Transmit(&uart_gimbal, (uint8_t*)buf, len, 100);

  }


  void setParameter(int id, int val){

      union intFloat parameterValue;
      parameterValue.i = val;
      
      mavlink_message_t msg;
      uint8_t buf[MAVLINK_MAX_PACKET_LEN];
      mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 180, 0, id, parameterValue.f, 0.0, 0.0, 0.0, 0.0, 0.0);
      uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
      HAL_UART_Transmit(&uart_gimbal, (uint8_t*)buf, len, 100);
        
  }



  void setAngles(float roll, float pitch, float yaw){
    
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 205, 0, pitch, roll, yaw, 0.0, 0.0, 0.0, 0.0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    HAL_UART_Transmit(&uart_gimbal, (uint8_t*)buf, len, 100);
      
  }


  void recenter(){
    
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 204, 0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    HAL_UART_Transmit(&uart_gimbal, (uint8_t*)buf, len, 100);
    
  }


  void setRc(byte type, uint16_t val){
    
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];

    union byteToInt tmpVal;
    tmpVal.i = val; 
    
    union byteToFloat data1;
    data1.bytes.b0 = 0xFA;
    data1.bytes.b1 = 0x02;
    data1.bytes.b2 = type;
    data1.bytes.b3 = tmpVal.bytes.b0;

    union byteToFloat data2;
    data2.bytes.b0 = tmpVal.bytes.b1;
    data2.bytes.b1 = 0;
    data2.bytes.b2 = 0;
    data2.bytes.b3 = 0;
    
    mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 1235, 0, data1.f, data2.f, 0.0, 0.0, 0.0, 0.0, 0.0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    HAL_UART_Transmit(&uart_gimbal, (uint8_t*)buf, len, 100);

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

#ifdef READ_FROM_GIMBAL

  void read_mavlink_storm32(){ 
    
    mavlink_message_t msg;
    mavlink_status_t status;
    
    requestAttitude();
  
    while (uart_gimbal.available() > 0) {
      
      uint8_t c = uart_gimbal.read();
      //trying to grab msg
      if (mavlink_parse_char(MAVLINK_COMM_0, c, &msg, &status)) {   
        switch (msg.msgid) {
          case MAVLINK_MSG_ID_ATTITUDE:
            {
              //get pitch and yaw angle from storm (requestAttitude() must be executed first)
              gimbalYaw = ToDeg(mavlink_msg_attitude_get_yaw(&msg));
              gimbalPitch = ToDeg(mavlink_msg_attitude_get_pitch(&msg));
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

#endif

void init_gimbal(void){
  setAngles(3, -30, 20);
  HAL_Delay(1000); // MS
  setAngles(0, 0, 0);
  HAL_Delay(1000); // MS
  setAngles(-3, 30, -20);
  HAL_Delay(1000); // MS
  setAngles(0, 0, 0);
  
}

