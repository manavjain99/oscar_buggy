/* 
 Author: Param Deshpande
 * Date created:  Sat 25 Apr 19:21:45 IST 2020
 * Description: 
 * Main file for the stm32 MCU responsilble for controlling the gimbal and the buggy.
 * mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed-os/mbed.h"

#include "include/commons.h"
#include "include/nucleo_ports.h"
#include "include/nucleo_uart.h"
//#include "include/gimbal_stuff.h"



/* PRIVATE VARIABLES */

static DigitalOut led(LED1);

/* PUBLIC VARIABLES */

/* FUNCTION PROTOTYPES */
void blink_ntimes(uint8_t );

int main(void){
    //setup 

    //blink_ntimes(3);
        
    //init_uart();
    //init_gimbal();

    while (1) {
            led = true;
    }
}

void blink_ntimes(uint8_t ntimes_){
    // flash LEDs so we know we are alive
    static DigitalOut led(LED1);
    for (uint16_t n = 0; n < ntimes_; n++) {
       led = true;
       ThisThread::sleep_for(200ms);
       led = false;
       ThisThread::sleep_for(200ms);
    }
}

