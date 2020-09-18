
#include "../mbed-os/mbed.h"
#include "../include/nucleo_ports.h"
#include "../include/nucleo_uart.h"

//BufferedSerial uart_gimbal(nucleo_tx_gimbal_pin, nucleo_rx_gimbal_pin);      //BOARD TX, RX
//BufferedSerial uart_obcomp(nucleo_tx_obcomp_pin, nucleo_rx_obcomp_pin);      //BOARD TX, RX
BufferedSerial uart_debugcon(nucleo_tx_stlink_pin, nucleo_rx_stlink_pin);      //BOARD TX, RX

//BufferedSerial serial_port(nucleo_tx_stlink_pin, nucleo_rx_stlink_pin);


void init_uart( BufferedSerial& serial_port){
    serial_port.set_baud(9600);
    serial_port.set_format(8,BufferedSerial::None,1);
}
