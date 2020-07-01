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

void setup(){

}
void loop(){
  
}
/*
//*DEFINE YOUR GLOBAL VARS HERE*

// If you change this make sure to change in .py in waitingforArduino function.

#include <iostream>
#include <random>
#include </usr/include/boost/math/interpolators/cubic_b_spline.hpp>
#include </usr/include/boost/random/mersenne_twister.hpp>
#include </usr/include/boost/random/uniform_real_distribution.hpp>


#define STM32_READY "<Arduino is ready>"
#define MS_TO_HZ(x) (1e3/x)
#define TICK_DURATION_MS (7.0)

static const byte times_flash_ = 3;

void setup()
{

    Serial.begin(115200);
  
    // tell the PC we are ready
   Serial.println("<Arduino is ready>");
}


void loop()
{
  //* Nothing to do all is done by hardware. Even no interrupt required. *

      // We begin with an array of samples:
    std::vector<double> v(6);
    // And decide on a stepsize:
    double step = 1;

    v[0] = 5;
    v[1] = 2.3;
    v[2] = 3;
    v[3] = 4.3;
    v[4] = 2.9;
    v[5] = 3.1;
    
    // make spline of size 6.
    boost::math::cubic_b_spline<double> spline(v.data(), v.size(), 0 /* start time *, step);

    // start from len/2 to len.
    
    long double ctr =0;
    while(ctr < 6){
        std::cout << spline(ctr) << "," << std::endl;
        ctr = ctr + 0.05;
    }

    // Remove first 3 and add 3 new vals.
    v[0] = v[3];
    v[1] = v[4];
    v[2] = v[5];
    v[3] = 5.3;
    v[4] = 2.0;
    v[5] = 1.6;


    std::cout << "done with old spline" << std::endl << std::endl ;
    // make a spline of size 6. ...

    boost::math::cubic_b_spline<double> spline2(v.data(), v.size(), 0 /* start time *, step);

    // start from len/2 to len.
    
    ctr =0;
    while(ctr < 6){
        std::cout << spline2(ctr) << "," << std::endl;
        ctr = ctr + 0.05;
    }
}
*/

#endif

#ifndef DEBUG
#include "../include/main.h"
#include "../include/commons.h"
#include "../include/uart.hpp"
#include "gimbal_stuff.h"

/*DEFINE YOUR GLOBAL VARS HERE*/

// If you change this make sure to change in .py in waitingforArduino function.
#define STM32_READY "<Arduino is ready>"
#define MS_TO_HZ(x) (1e3/x)
#define TICK_DURATION_MS (10.0)

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

    // Setting up the tick based ISR.
     #if defined(TIM1)
      TIM_TypeDef *Instance = TIM1;
    #else
      TIM_TypeDef *Instance = TIM2;
    #endif

  // Instantiate HardwareTimer object. Thanks to 'new' instanciation, HardwareTimer is not destructed when setup() function is finished.
  HardwareTimer *MyTim = new HardwareTimer(Instance);

  // configure pin in output mode
  pinMode(pin, OUTPUT);

  MyTim->setOverflow(MS_TO_HZ(TICK_DURATION_MS), HERTZ_FORMAT); 
  MyTim->attachInterrupt(Update_IT_callback);
  MyTim->resume();

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

