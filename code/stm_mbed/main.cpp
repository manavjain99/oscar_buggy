/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed-os/mbed.h"


#define MAXIMUM_BUFFER_SIZE                                                  32

// Create a DigitalOutput object to toggle an LED whenever data is received.
static DigitalOut led(LED1);

// Create a BufferedSerial object with a default baud rate.
static BufferedSerial serial_port(PA_9, PA_10);

int main(void)
{
    // Set desired properties (9600-8-N-1).
    serial_port.set_baud(9600);
    serial_port.set_format(
        /* bits */ 8,
        /* parity */ BufferedSerial::None,
        /* stop bit */ 1
    );

    // Application buffer to receive the data
    char buf[MAXIMUM_BUFFER_SIZE] = {0};

    while (1) {
            led = true;

        if (uint32_t num = serial_port.read(buf, sizeof(buf))) {
            // Toggle the LED.

            // Echo the input back to the terminal.
            serial_port.write(buf, num);
        }
    }
}
