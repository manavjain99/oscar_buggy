
#include "../mbed-os/mbed.h"
#include "../include/nucleo_uart.h"
#include "../include/nucleo_ports.h"

//BufferedSerial uart_debugcon (nucleo_tx_stlink_pin, nucleo_rx_stlink_pin);      //BOARD TX, RX
BufferedSerial serial_port(nucleo_tx_stlink_pin, nucleo_rx_stlink_pin);

void init_uart( BufferedSerial& serial_port){
    serial_port.set_baud(9600);
    serial_port.set_format(8,BufferedSerial::None,1);
}
