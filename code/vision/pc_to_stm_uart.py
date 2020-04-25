import serial

serialPort = serial.Serial(port = '/dev/ttyUSB0', baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
#ser = serial.Serial('/dev/ttyUSB0')  # open serial port
serialString = ""                           # Used to hold data coming over UART


while(1):
    test_var = ' '
    # Wait until there is data waiting in the serial buffer
    output_var = str(test_var) + '\r\n'
    serialPort.write(output_var.encode())
    #serialPort.write(b"\r\n")


    #if(serialPort.in_waiting > 0):
#
    #    # Read data out of the buffer until a carraige return / new line is found
    #    serialString = serialPort.readline()
    #    print(serialString)
    #    # Print the contents of the serial data
    #    #print(str(serialString.decode('Ascii')))
    #    if(serialString == b'STM_READY\r\n'):
    #        #serialPort.write(test_var)
    #        serialPort.write(b"ACK\r\n")
        # Stop reading if ACK is true.
        #break
        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        #serialPort.write(b"Thank you for sending data, sent from python \r\n")

