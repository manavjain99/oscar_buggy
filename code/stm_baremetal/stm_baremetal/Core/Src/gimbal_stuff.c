/*
 * gimbal_stuff.c
 *
 *  Created on: Aug 13, 2020
 *      Author: Param Deshpande
 */


#include "../Inc/main.h"
#include "../Inc/global.h"
#include "../Inc/gimbal_stuff.h"
#include "../Inc/curves.h"

/*SET PARAMETERS */
#define CURVES_TO_CONSIDER 5
#define MAX_HYPERFRAME_TIME 400UL /* MS, time before next UART interrupt */
#define INTERPOLATION_PTS 2



/*DONT TOUCH THESE , UNLESS YOU KNOW WHAT YOU ARE DOING*/
#define uart_gimbal huart6
#define CURVES_TO_CONSIDER_INDEX (CURVES_TO_CONSIDER-1)
#define MAX_FIRES (CURVES_TO_CONSIDER*INTERPOLATION_PTS)

/* GLobal Vars */
uint32_t gimbalHyperframeTime = 0;

/* Private Macros */
#define getCurveVal(x,d,c,b,a) (d*pow(x,3) + c*pow(x,2) + b*pow(x,1) + a)

/* Private Vars */
static int8_t curveIndex = -1; // LET IT BE -1 
static uint16_t firingTime = 0;
static float_t time1Curve = (INTERPOLATION_PTS!=0)?(MAX_HYPERFRAME_TIME/(float_t)(CURVES_TO_CONSIDER)):(0);
static float_t curveAngleRoll = 0;
static float_t curveAnglePitch = 0;
static float_t curveAngleYaw = 0;
static float_t curveX = 0;
static  uint8_t no_of_fires = MAX_FIRES;

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
/*NOT MODIFIED , NOT COMPILABLE */
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

void getFiringTime(void){
  //no_of_fires & MAX_HYPERFRAME_TIME
  firingTime = (MAX_FIRES % no_of_fires)*(MAX_HYPERFRAME_TIME/(float)MAX_FIRES);
}

void getFiringVals(void){
   // Goes from 0 to INTERPOLATION_PTS - 1
   float_t cyclicVar = (no_of_fires) % INTERPOLATION_PTS; 
   float_t x = cyclicVar/(float_t)(INTERPOLATION_PTS);
   if( (int8_t)(cyclicVar) == 0 ){
     curveIndex++;
   }
    curveAngleRoll = getCurveVal(x,roll.curves[curveIndex].d,roll.curves[curveIndex].c,roll.curves[curveIndex].b,roll.curves[curveIndex].a);
    curveAnglePitch = getCurveVal(x,pitch.curves[curveIndex].d,pitch.curves[curveIndex].c,pitch.curves[curveIndex].b,pitch.curves[curveIndex].a);
    curveAngleYaw = getCurveVal(x,yaw.curves[curveIndex].d,yaw.curves[curveIndex].c,yaw.curves[curveIndex].b,yaw.curves[curveIndex].a);
   
}
void actuate_gimbal(void){
  gimbalHyperframeTime = 0;
  firingTime = 0;
  no_of_fires = CURVES_TO_CONSIDER*INTERPOLATION_PTS;
  curveIndex = -1;
   
  while(no_of_fires){
    getFiringTime();
    getFiringVals();
    // Wait until it is time to fire. 
    while(  (gimbalHyperframeTime <= firingTime)  && (gimbalHyperframeTime <= MAX_HYPERFRAME_TIME));
    setAngles(curveAngleRoll,curveAnglePitch,curveAngleYaw);
    printf("Roll:%f ,Pitch:%f, Yaw:%f \n", curveAngleRoll, curveAnglePitch, curveAngleYaw );
    no_of_fires--;
  }
}

/*
void actuate_gimbal(void){
  assert(INTERPOLATION_PTS!=0);
  gimbalHyperframeTime = 0;
  float_t x = 0;
  curveIndex = 0;
  firingTime  = 0;

  while(gimbalHyperframeTime <= MAX_HYPERFRAME_TIME){
    //ITM_Port32(0) = 3;

    if(gimbalHyperframeTime >= firingTime){
    
    curveAngleRoll = getCurveVal(x,roll.curves[curveIndex].d,roll.curves[curveIndex].c,roll.curves[curveIndex].b,roll.curves[curveIndex].a);
    curveAnglePitch = getCurveVal(x,pitch.curves[curveIndex].d,pitch.curves[curveIndex].c,pitch.curves[curveIndex].b,pitch.curves[curveIndex].a);
    curveAngleYaw = getCurveVal(x,yaw.curves[curveIndex].d,yaw.curves[curveIndex].c,yaw.curves[curveIndex].b,yaw.curves[curveIndex].a);
    
    printf("\nCoeffs dcba yaw are: %f, %f, %f, %f", yaw.curves[curveIndex].d, yaw.curves[curveIndex].c, yaw.curves[curveIndex].b, yaw.curves[curveIndex].a);
    setAngles(curveAngleRoll,curveAnglePitch,curveAngleYaw);
    //printf("Roll:%f ,Pitch:%f, Yaw:%f \n", curveAngleRoll, curveAnglePitch, curveAngleYaw );
    firingTime += time1Curve/((float_t)(INTERPOLATION_PTS));
    x += 1/(float)(INTERPOLATION_PTS);
    }
    if(firingTime >= (curveIndex+1)*(time1Curve)){
    	curveIndex += (1);
    	x =0;
    }
    //ITM_Port32(0) = 4;
  }
  gimbalHyperframeTime = 0;
  firingTime  = 0;
}
*/
