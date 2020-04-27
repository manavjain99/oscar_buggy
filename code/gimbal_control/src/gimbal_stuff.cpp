/*
* Author: Param Deshpande
* Date created:  Mon 27 Apr 13:06:16 IST 2020
* Description: 
* deals with controlling the gimbal according to object params ie object_cx and object_cy.
* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------
*/
#include "main.h"
#include "commons.h"
#include "gimbal_stuff.h"
#include "uart.hpp"
#include "utils.h"
#include "../mavlink/include/mavlink_types.h"
#include "../mavlink/include/mavlink.h"

/*DEFINE YOUR GLOBAL VARS HERE*/

#define ToDeg(x) (x*57.2957795131)  // *180/pi
#define INCREASING HIGH
#define DECREASING LOW

float gimbal_roll = 0.0;
float gimbal_pitch = 0.0;
float gimbal_yaw = 0.0;

/*DEFINE YOUR PRIVATE VARS HERE*/
static String gimbal_object_params_ = "";

static float obj_pos1x_ = 0.0;
static float obj_pos1y_ = 0.0;

static float obj_pos2x_ = 0.0;
static float obj_pos2y_ = 0.0;

static float xpix_per_deg_ = 0.0;
static float ypix_per_deg_ = 0.0;


static bool state = LOW;
static int test_angle = 0;
static bool angle_status = INCREASING;

/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/


/* START YOUR CODE HERE */

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
    uart_gimbal.write(buf, len);
  
  }

  void requestParameter(int id){
      
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_param_request_read_pack(255, 1, &msg, 71, 67, "", id);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    uart_gimbal.write(buf, len);   
    
  }

  void setParameter(int id, int val){

      intFloat parameterValue;
      parameterValue.i = val;
      
      mavlink_message_t msg;
      uint8_t buf[MAVLINK_MAX_PACKET_LEN];
      mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 180, 0, id, parameterValue.f, 0.0, 0.0, 0.0, 0.0, 0.0);
      uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
      uart_gimbal.write(buf, len); 
        
  }


  void setAngles(float roll, float pitch, float yaw){
    
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 205, 0, pitch, roll, yaw, 0.0, 0.0, 0.0, 0.0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    uart_gimbal.write(buf, len);
    
  }

  void recenter(){
    
    mavlink_message_t msg;
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    mavlink_msg_command_long_pack(255, 1, &msg, 71, 67, 204, 0, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &msg);
    uart_gimbal.write(buf, len);
    
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
    uart_gimbal.write(buf, len);  
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




void get_pix_per_deg(void){
    
  read_mavlink_storm32();
  setAngles(0,0,-90);
    // Set to -45 deg.
  //while(gimbal_yaw != 90.0F){
  //  ++gimbal_yaw;
  //  setAngles(-gimbal_roll, -gimbal_pitch, -gimbal_yaw);
  //  delay(50);
  //}
  //  setAngles(-gimbal_roll, -gimbal_pitch, -90.0F);
  //  delay(50);
    /*
    gimbal_yaw = -45.0;
    setAngles(-gimbal_roll, -gimbal_pitch, -gimbal_yaw);*
    
    // Wait for obj to be detected.
    while((object_cx == -1 ) && (object_cy == -1 )){
        gimbal_object_params_ = rec_and_ack("ACK_OC");
        get_object_params(gimbal_object_params_);
    }

    // get obj position1 .
    gimbal_object_params_ = rec_and_ack("ACK_OC");
    get_object_params(gimbal_object_params_);
    obj_pos1x_ = object_cx; 
    obj_pos1y_ = object_cy; 

    // increase yaw until +45 deg.
    gimbal_yaw = 45.0;
    setAngles(-gimbal_roll, -gimbal_pitch, -gimbal_yaw);
    
    // Get obj position2.
    gimbal_object_params_ = rec_and_ack("ACK_OC");
    get_object_params(gimbal_object_params_);
    obj_pos2x_ = object_cx; 
    obj_pos2y_ = object_cy; 

    // pix/deg = (pos2 - pos1 )/90
    xpix_per_deg_ = (obj_pos2x_ - obj_pos1x_ )/(90.0F);    
    ypix_per_deg_ = (obj_pos2y_ - obj_pos1y_ )/(90.0F);
  */
}

/* END OF FILE */

