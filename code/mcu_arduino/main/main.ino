/*
* Author: Param Deshpande
* Date created:  Sat 25 Apr 19:21:45 IST 2020
* Description: 
* Main file for the stm32 MCU responsilble for controlling the gimbal and the buggy.
* License :
* ------------------------------------------------------------
* "THE BEERWARE LICENSE" (Revision 42):
* Param Deshpande wrote this code. As long as you retain this 
* notice, you can do whatever you want with this stuff. If we
* meet someday, and you think this stuff is worth it, you can
* buy me a beer in return.
* ------------------------------------------------------------
*/
//#define DEBUG

#ifdef DEBUG 

#include "../include/main.h"
#include "../include/commons.h"
#include "../include/uart.hpp"
#include "gimbal_stuff.h"
//#include "boost/math/interpolators/cubic_b_spline.hpp"
#include "InterpolationLib.h"

void setup()
{

}

void loop()
{
  
}

#endif

#ifndef DEBUG33 // Basically runs every time remove 33 if need to trest above debug part code
//#include "../include/main.h"
#include "../include/commons.h"
#include "../include/uart.hpp"
#include "../include/gimbal_stuff.h"

/*DEFINE YOUR GLOBAL VARS HERE*/

// If you change this make sure to change in .py in waitingforArduino function.
#define STM32_READY "<Arduino is ready>"
#define MS_TO_HZ(x) (1e3/x)

float frame_ht = -1.0F;
float frame_wd = -1.0F;

float object_area = -1.0F;
float object_cx   = -1.0F;
float object_cy   = -1.0F;

float new_msg_time_MS = -1;  // Used to calc spline interval 
float old_msg_time_MS = 1;

static bool run_once_ = true;
static double old_time_MS_ = 0;
static double new_time_MS_ = 0;
static double del_time_MS_ = 0;

static double overflowCheckTime_ = -1;

/*DEFINE YOUR PRIVATE VARS HERE*/

static const byte times_flash_ = 3;
static bool led_debug_state_ = false;
static int debug_area_ = 99;
/*DEFINE YOUR PRIVATE FUNCTION PROTOTYPES HERE*/


/* START YOUR CODE HERE */

#if !defined(STM32_CORE_VERSION) || (STM32_CORE_VERSION  < 0x01090000)
//#error "Due to API change, this sketch is compatible with STM32_CORE_VERSION  >= 0x01090000"
#endif

#if defined(LED_BUILTIN)
#define pin  LED_BUILTIN
#else
#define pin  D2
#endif

//void Update_IT_callback(HardwareTimer*);


void Update_IT_callback(HardwareTimer* TIM1ptr){
    

    old_time_MS_ = millis();
    // takes x msecs to run. Gives me new data.
    rcv_obcomp();
    led_debug_state_  = HIGH;
    orient_gimbal();  
     

    if(newDataFromPC == true){
      //Set gimbal angles.
      // Ack that you moved the gimbal.


      //led_debug_state_ = !led_debug_state_;
      ack_obcomp();


      // ack_obcomp clears theflag but still as a safety measure.
    }
    
    //if(object_area == 100.0F){
    //  led_debug_state_ = !led_debug_state_;
    //led_debug_state = HIGH;
    //digitalWrite(LED_BUILTIN, led_debug_state_);
    //}
    new_time_MS_ = millis();
    del_time_MS_ = new_time_MS_ - old_time_MS_;
  
    //orient_gimbal();    
}

void setup(void){

    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);


    // flash LEDs so we know we are alive
    for (byte n = 0; n < times_flash_; n++) {
       digitalWrite(LED_BUILTIN, HIGH);
       delay(200);
       digitalWrite(LED_BUILTIN, LOW);
       delay(200);
       
    }

    
    
    init_uart();
    //init_gimbal();

  // configure pin in output mode
  pinMode(pin, OUTPUT);

  //MyTim->setOverflow(MS_TO_HZ(TICK_DURATION_MS), HERTZ_FORMAT); 
  //MyTim->attachInterrupt(Update_IT_callback);
  //MyTim->resume();

    // flash LEDs so we know we are alive
    for (byte n = 0; n < times_flash_; n++) {
       digitalWrite(LED_BUILTIN, HIGH);
       delay(200);
       digitalWrite(LED_BUILTIN, LOW);
       delay(200);
       
    }
    
    
    init_uart();
    //init_gimbal();


    old_time_MS_ = millis();

    uart_obcomp.println("<Arduino is ready>");
    uart_debugcon.println("Setup complete ");


}

void loop(){

  if(run_once_ == true){
    old_time_MS_ = millis();
    //read_mavlink_storm32();
    //setAngles(0,0,-45);
    //delay();
    // setAngles(0,2,45);//1
    // setAngles(0,5,47);
    //setAngles(0,7,50);//3
    //setAngles(0,10,53);
    //setAngles(0,2,55);//5
    //setAngles(0,2,58);
    //setAngles(0,2,61);//7
    //setAngles(0,2,64); 
    //setAngles(0,2,67);//9
    //setAngles(0,2,70);
    //read_mavlink_storm32();
    new_time_MS_ = millis();
    run_once_ = false;

  }
  new_time_MS_ = millis();
  del_time_MS_ = new_time_MS_ - old_time_MS_;
  if(del_time_MS_ > TICK_DURATION_MS){
    old_time_MS_ = millis();
    /***********Enter your code here*******/
    rcv_obcomp();
    orient_gimbal(); 
    if(newDataFromPC == true){
      digitalWrite(pin,!digitalRead(pin));
      new_msg_time_MS = millis() - old_msg_time_MS;
      old_msg_time_MS = millis();
      ack_obcomp();  // Clears the flag
    }
    /**************************************/
    overflowCheckTime_ = millis() - old_time_MS_;
    if(overflowCheckTime_ > TICK_DURATION_MS){
      while (1){
        /* code */
        uart_debugcon.print("Tick overflow, took ");
        uart_debugcon.print(overflowCheckTime_);
        uart_debugcon.print("MS for a TICK TIME OF ");
        uart_debugcon.print(TICK_DURATION_MS);
        uart_debugcon.println("MS please increase tick interval ");

      }
      
    }
  }
  //uart_obcomp.println(del_time_MS_);
  //uart_obcomp.print(" ");
  //uart_obcomp.println(gimbalYaw);

}

#endif

/* END OF FILE */

