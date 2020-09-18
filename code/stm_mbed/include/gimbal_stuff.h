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
#ifndef gimbal_stuff_h
#define gimbal_stuff_h


/* EXTERN YOUR GLOBAL VARS HERE*/

extern double gimbalYaw ;
extern double gimbalPitch ;


extern int del_gimbal_roll ;
extern int del_gimbal_pitch;
extern int del_gimbal_yaw  ;

extern float a2x ;
extern float b2x ;
extern float c2x ;
extern float d2x ;
              
extern float a2y ;
extern float b2y ;
extern float c2y ;
extern float d2y ;



extern float a3x ;
extern float b3x ;
extern float c3x ;
extern float d3x ;
              
extern float a3y ;
extern float b3y ;
extern float c3y ;
extern float d3y ;




extern float a4x ;
extern float b4x ;
extern float c4x ;
extern float d4x ;
              
extern float a4y ;
extern float b4y ;
extern float c4y ;
extern float d4y ;


/* DEFINE YOUR GLOBAL FUNCTION OR TASKS PROTOTYPES HERE*/
void init_gimbal(void);
void orient_gimbal(void);
void setAngles(float , float , float );
void read_mavlink_storm32();
#endif


/* END OF FILE */

