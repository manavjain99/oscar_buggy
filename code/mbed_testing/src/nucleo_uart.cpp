//#include "../include/commons.h"

#include "../mbed-os/mbed.h"
#include "../include/nucleo_uart.h"
#include "../include/nucleo_ports.h"

/*DEFINE YOUR GLOBAL VARS HERE*/


/*DEFINE YOUR PRIVATE VARS HERE*/
BufferedSerial uart_gimbal (nucleo_rx_gimbal_pin, nucleo_tx_gimbal_pin);  //Board RX, TX
BufferedSerial uart_debugcon (nucleo_rx_stlink_pin, nucleo_tx_stlink_pin);  //Board RX, TX
BufferedSerial uart_obcomp(nucleo_rx_obcomp_pin, nucleo_rx_obcomp_pin);



void init_uart(void){
    uart_obcomp.set_baud(115200);
    uart_debugcon.set_baud(115200);
    uart_gimbal.set_baud(115200);   

    uart_obcomp.set_format(
        /* bits */ 8,
        /* parity */ BufferedSerial::None,
        /* stop bit */ 1
    );
    uart_debugcon.set_format(
        /* bits */ 8,
        /* parity */ BufferedSerial::None,
        /* stop bit */ 1
    );
    uart_gimbal.set_format(
        /* bits */ 8,
        /* parity */ BufferedSerial::None,
        /* stop bit */ 1
    );

}
