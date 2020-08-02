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
*///

#include "../include/commons.h"
#include "../include/gimbal_stuff.h"
#include "../include/nucleo_uart.h"
#include "../mavlink/include/mavlink_types.h"
#include "../mavlink/include/mavlink.h"

/*DEFINE YOUR GLOBAL VARS HERE*/

// these vars are parsed from uart.
int del_gimbal_roll  = 0;
int del_gimbal_pitch = 0;
int del_gimbal_yaw   = 0;

float new_msg_time_MS = 0;


float a2x = 0 ;
float b2x = 0 ;
float c2x = 0 ;
float d2x = 0 ;   

float a2y = 0 ;
float b2y = 0 ;
float c2y = 0 ;
float d2y = 0 ;


float a3x = 0 ;
float b3x = 0 ;
float c3x = 0 ;
float d3x = 0 ;

float a3y = 0 ;
float b3y = 0 ;
float c3y = 0 ;
float d3y = 0 ;


float a4x = 0 ;
float b4x = 0 ;
float c4x = 0 ;
float d4x = 0 ;

float a4y = 0 ;
float b4y = 0 ;
float c4y = 0 ;
float d4y = 0 ;


/* MAKE SURE THIS MATCHES WITH MAIN.PY file*/
#define NO_OF_TRAJ_PTS 3

/* Multiples of 3 */
#define MAX_GIMBAL_YAW 42
#define MAX_GIMBAL_PITCH 12
#define MAX_GIMBAL_ROLL 9

#define ToDeg(x) (x*57.2957795131)  // *180/pi
#define INCREASING HIGH
#define DECREASING LOW

static double timeStep_ = 0;

double gimbalYaw = 0;
double gimbalPitch = 0;

/*DEFINE YOUR PRIVATE VARS HERE*/
// Returns bounding angle if current ang(x) crosses bounding ang(y) else returns current ang(x)
#define CHECK_MAX(x,y) ((abs(x)>y) ? ((x>0)?(y):(-y)) : (x)  )

// If you change this you need to change the entire Gimbal Math as well.
#define SIGNAL_UPDATE_MS 330.0F


static int inst_gimbal_roll_ = 0;
static int inst_gimbal_pitch_ = 0;
static int inst_gimbal_yaw_ = 0;

static int total_gimbal_roll_ = 0;
static int total_gimbal_pitch_ = 0;
static int total_gimbal_yaw_ = 0;


static int pt_num_ = 0;



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
    char buf[64] = {0};
    requestAttitude();
  
    while (uart_obcomp.readable() > 0) {
      
      uint8_t c = uart_gimbal.read(buf, sizeof(buf));
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

void init_gimbal(void){
  setAngles(3, -30, 20);
  ThisThread::sleep_for(500ms);
  setAngles(total_gimbal_roll_, total_gimbal_pitch_, total_gimbal_yaw_);
  ThisThread::sleep_for(500ms);
  setAngles(-3, 30, -20);
  ThisThread::sleep_for(500ms);
  setAngles(total_gimbal_roll_, total_gimbal_pitch_, total_gimbal_yaw_);
  ThisThread::sleep_for(500ms);

  read_mavlink_storm32();

}

// I have gimbal delta roll,pitch,yaw. 
/**
 * @input : 4 coeffs of the splines.
 * @breif : Creates / tells what delta Angs need to be followed for each yaw/pitch.
 * @output : Modifies del_gimbal_angs  
*/
//#define DEBUG_GIMBALMATH
void gimbal_math(void){
    // If there is a new message init case. or done with the current message.
    #ifndef DEBUG_GIMBALMATH
    if(new_msg_time_MS != -1){
      del_gimbal_yaw   = a2x + b2x*(timeStep_/new_msg_time_MS) + c2x*pow((timeStep_/new_msg_time_MS),2) + d2x*pow((timeStep_/new_msg_time_MS),3);  
      
      del_gimbal_pitch = a2y + b2y*(timeStep_/new_msg_time_MS) + c2y*pow((timeStep_/new_msg_time_MS),2) + d2y*pow((timeStep_/new_msg_time_MS),3);  
      timeStep_ += TICK_DURATION_MS;
    }
    else {
      del_gimbal_yaw = 0;
      del_gimbal_pitch = 0;
    }
    #ifdef UART_DEBUG
    string debugMsg = "refresh time ";

    //debugMsg = "refresh time ";
    //uart_debugcon.write(debugMsg , sizeof(debugMsg));
    //debugMsg = to_string(new_msg_time_MS);
    //uart_debugcon.write(debugMsg , sizeof(debugMsg));
    
    //uart_debugcon.write(debugMsg , sizeof(debugMsg));
//
    //uart_debugcon.print(" ");
    //uart_debugcon.print("timestep ");
    //uart_debugcon.println(timeStep_);

    #endif 
  if(newDataFromPC == true || timeStep_ > new_msg_time_MS){
  timeStep_ = 0.0F;
  }
  #endif

  #ifdef DEBUG_GIMBALMATH
      del_gimbal_yaw   = a2x + b2x*(1) + c2x*pow((1),2) + d2x*pow((1),3);  
      del_gimbal_pitch = a2y + b2y*(1) + c2y*pow((1),2) + d2y*pow((1),3);  


  #endif

}


void orient_gimbal(void){

  /*
   * @input : Reads delta gimbal angs.
   * @brief : Moves gimbal according to the delta gimbal angs, bounds it. And a change of ref frame 
   * @output : Actuates the GIMBAL.
   */ 
  //++pt_num_;
//

  // Takes care of updating delta angles. 
  gimbal_math();
  #ifndef DEBUG_GIMBALMATH
  
  inst_gimbal_roll_  += del_gimbal_roll;
  inst_gimbal_pitch_ += del_gimbal_pitch;
  inst_gimbal_yaw_   += del_gimbal_yaw;

  inst_gimbal_roll_  = CHECK_MAX(inst_gimbal_roll_, MAX_GIMBAL_ROLL);
  inst_gimbal_pitch_ = CHECK_MAX(inst_gimbal_pitch_, MAX_GIMBAL_PITCH);
  inst_gimbal_yaw_   = CHECK_MAX(inst_gimbal_yaw_, MAX_GIMBAL_YAW);
  
  #ifdef UART_DEBUG
  //string debugMsg = "inst yaw ";
  //debugMsg.append(to_string(inst_gimbal_yaw_));
  //uart_debugcon.print("total pitch");
  //uart_debugcon.print(" ");
  //uart_debugcon.print(total_gimbal_pitch_);
  //uart_debugcon.print(" ");
  
  //uart_debugcon.print("total yaw");
  //uart_debugcon.print(" ");
  //uart_debugcon.print(total_gimbal_yaw_);
  //uart_debugcon.print(" ");
  
  //uart_debugcon.print("instn pitch");
  //uart_debugcon.print(" ");
  //uart_debugcon.print(inst_gimbal_pitch_);
  //uart_debugcon.print(" ");
  
  //uart_debugcon.write(debugMsg,sizeof(debugMsg));
  //uart_debugcon.print("inst yaw");
  //uart_debugcon.print(" ");
  //uart_debugcon.print(inst_gimbal_yaw_);
  //uart_debugcon.print(" ");
  
  //uart_debugcon.print("del pitch");
  //uart_debugcon.print(" ");
  //uart_debugcon.print(del_gimbal_pitch);
  //  //uart_debugcon.print(" ");
    //
  //  uart_debugcon.print("del yaw");
    ////uart_debugcon.print(" ");
    //uart_debugcon.print(del_gimbal_yaw);
  //  
  //uart_debugcon.println(" ");
    
  #endif 

  setAngles(inst_gimbal_roll_, inst_gimbal_pitch_, inst_gimbal_yaw_);
  
  // The issue : 
  // Haven't referenced the change in angle meas by the obcomp when the gimbal is moving.
  
  // Now my refernce axis may have been changed. Just Balancing that 
  // Assuming gimbal tracked that part now new ref will be where the axis is in the new msg.
  if(newDataFromPC == true){

    //total_gimbal_roll_  += del_gimbal_roll ;     
    //total_gimbal_pitch_ += del_gimbal_pitch  ;
    //total_gimbal_yaw_   += del_gimbal_yaw  ;    

  }
  #endif

  #ifdef DEBUG_GIMBALMATH
  if(newDataFromPC == true){
  setAngles(inst_gimbal_roll_, del_gimbal_pitch, del_gimbal_yaw);
  }
  #endif
}


void get_pix_per_deg(void){
    
  //read_mavlink_storm32();
  //setAngles(-gimbal_roll, -gimbal_pitch, -gimbal_yaw);
  //setAngles(0,0,-90);
    // Set to -45 deg.
  //while(gimbal_yaw != 90.0F){
  //  ++gimbal_yaw;
  //  setAngles(-gimbal_roll, -gimbal_pitch, -gimbal_yaw);
  //  delay(75);
  //}
   // setAngles(-gimbal_roll, -gimbal_pitch, -90.0F);
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

