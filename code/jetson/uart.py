"""
 Author: Param Deshpande
 Date created:  Sun 26 Apr 14:12:01 IST 2020
 Description: 
 uart comm betn obpc and mcu
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Sun 26 Apr 14:12:01 IST 2020
"""

#import 
#import 

import serial
uart_stm = serial.Serial(port = '/dev/ttyUSB0', baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
  

#if __name__ == '__main__':
  #import 
  #import 

""" WRITE YOUR FUNCTIONS HERE """

def init_uart_port(portname):
  """
  (str) -> (SerialPort)
  Description: inits UART params.
  >>>
  
  """

  import serial
  portname = serial.Serial(port = '/dev/ttyUSB0', baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
  #print(type(serialPort))
  return portname


def send_until_ack(send_message, ack_message, portname = uart_stm):
  """
  (str), (str), (SerialPort) -> (NoneType)
  Description: keep sending message until ack message is received.
  >>> send_until_ack(portname, send_message, ack_message)  
  """
  send_message = str(send_message) + '\r\n'
  ack_message  =  str(ack_message) + '\r\n'
  ack_message = bytes(ack_message, encoding = 'utf-8')
  rec_message = ''
  
  while(1):
    # Keep sending the message.
    portname.write(send_message.encode())

    # check if ack message received.
    if(portname.in_waiting > 0):
      rec_message = portname.readline()
     
    # If received message == ack message, then exit.
    if(rec_message == ack_message):
      break


def rec_and_ack(ack_message, portname = uart_stm):
  """
  (str), (SerialPort) -> (str)
 
  Description : 
  returns a string message, once received a message sends a ack message.
  
  >>> new_message = rec_and_ack(portname, ack_message)
  >>> new_message 
  ACK_FH
  """
  rec_message = ""
  ack_message = str(ack_message) + '\r\n'

  # mostly it should send in one go. If fails prints debug message on console.
  while (1):
    # Wait until there is data waiting in the serial buffer
    if(portname.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        rec_message = portname.readline()
        portname.write(ack_message.encode())
        return rec_message

    print("struck in rec_and_ack")
    






""" START YOUR CODE HERE """

if __name__ == '__main__':
  #uart_stm = init_uart_port()

  print("Waiting for communication...")
  # wait for stm to be ready.
  while (rec_and_ack("ACK") != b'STM_READY\r\n'):
      pass

  print("STM READY, Successfully read.")
  
  # send frame ht
  send_until_ack("99", "ACK_FH")
  print(" Sent frame ht successfully.")
  
  # send frame wd
  send_until_ack("909", "ACK_FW")
  print(" Sent frame wd successfully.")
  
  while (1):
    # send obj center
    send_until_ack("100, 25, 2", "ACK_OC")
    #print(rec_and_ack("ACK"))
    #print(" Sent object params successfully.")
    
  #import doctest
  #doctest.testmod()




""" END OF FILE """

