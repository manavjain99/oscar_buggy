/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include <string>
#include <iostream>
//#include "../include/main.h"
//#include "../include/commons.h"
//#include "../include/uart.hpp"
//#include "gimbal_stuff.h"
#include "../include/nucleo_ports.h"
#include "../include/nucleo_uart.h"
// Blinking rate in milliseconds
#define BLINKING_RATE     500ms

#define MAXIMUM_BUFFER_SIZE                                                  32

// Create a DigitalOutput object to toggle an LED whenever data is received.
static DigitalOut led(LED1);

// Create a BufferedSerial object with a default baud rate.
static BufferedSerial serial_port(nucleo_tx_obcomp_pin, nucleo_rx_obcomp_pin);
void blink_ntimes(uint8_t );

extern  BufferedSerial uart_gimbal ;
extern  BufferedSerial uart_obcomp ;
extern  BufferedSerial uart_debugcon;
int main()
{
    // Initialise the digital pin LED1 as an output
    DigitalOut led(LED1);
    // Set desired properties (9600-8-N-1).
    blink_ntimes(10);
    //serial_port.set_baud(9600);
    //serial_port.set_format(8,BufferedSerial::None,1);
    init_uart(uart_debugcon);
    //init_uart(uart_obcomp);
    //init_uart(uart_gimbal);
    
    char buf[MAXIMUM_BUFFER_SIZE] = "Hello World2! \n";;
    //buf = 
    while (true) {

        led = !led;
        //serial_port.write(buf, sizeof(buf));
        uart_debugcon.write(buf, sizeof(buf));
        ThisThread::sleep_for(BLINKING_RATE);
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


