/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include "include/nucleo_uart.h"
#include <string>
#include <iostream>
//#include "../include/main.h"
//#include "../include/commons.h"
//#include "../include/uart.hpp"
//#include "gimbal_stuff.h"

// Blinking rate in milliseconds
#define BLINKING_RATE     500ms

#define MAXIMUM_BUFFER_SIZE                                                  32

// Create a DigitalOutput object to toggle an LED whenever data is received.
static DigitalOut led(LED1);

// Create a BufferedSerial object with a default baud rate.
//static BufferedSerial serial_port(PA_9, PA_10);
void blink_ntimes(uint8_t );


int main()
{
    // Initialise the digital pin LED1 as an output
   // DigitalOut led(LED1);
      // Set desired properties (9600-8-N-1).
    blink_ntimes(10);
    init_uart();
    char buf[] = "debugMsg.c_str()\r\n";
    while (true) {
        led = !led;
        ThisThread::sleep_for(BLINKING_RATE);
        uart_debugcon.write(buf, sizeof(buf));

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

