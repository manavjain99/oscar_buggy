
"""
 Author: Param Deshpande
 Date created:  Mon Oct 12 20:35:48 IST 2020
 Description: 
 Sends 'hi' packet equivalents to gopro, basically makes sure gopro keeps sending udp packets and doesnt go to sleep
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Mon Oct 12 20:35:48 IST 2020
"""

#import 
#import 
import time
import socket
import subprocess
import struct 
import math
import base64
import sys
import ssl
import datetime
import struct
import subprocess
from socket import timeout
import time
import socket
import urllib.request
import json
import re
#if __name__ == '__main__':
  #import 
  #import 


LOCALHOST_STREAM_URI = "udp://127.0.0.1:10000"
HOST_STREAM_URI = "udp://198.168.0.105:10000" # this aint localhost, Im using this for testing
ip_addr = "10.5.5.9"
""" WRITE YOUR FUNCTIONS HERE """



def get_gopro_stream(stream_uri):
  """
  () -> ()
  Description: ffmpeg values for better parsing and sending stuff to respective uri
  >>>
  
  """
  subprocess.Popen("ffmpeg -f mpegts -i udp://10.5.5.9:8554" +
  " -an -map 0:v  -c:v h264 -profile:v high444 -pix_fmt yuvj420p -f mpegts -deinterlace -s 848x480 -b 500k -r 29.97 " + 
  stream_uri, shell=True)


def keep_gopro_alive():
  """
  () -> ()
  Description: keeps gopro alive
  >>>
  
  """
  keep_alive_payload = "_GPHD_:0:0:2:0.000000\n".encode()
  while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(keep_alive_payload, (ip_addr, 8554))
    time.sleep(2500/1000)



def gopro_thread():
  """
  () -> ()
  Description: gets gopros output to the local host or the uri to transmit.
  >>>
  
  """
  power_on()
  get_gopro_stream(HOST_STREAM_URI)
  keep_gopro_alive()

""" START YOUR CODE HERE """

if __name__ == '__main__':
  pass
  #import doctest
  #doctest.testmod()
  #-gopro_thread()
  keep_gopro_alive()
  
  
   
""" END OF FILE """

