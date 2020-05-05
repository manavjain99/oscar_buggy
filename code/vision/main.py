"""
 Author: Param Deshpande
 Date created:  Mon 27 Apr 18:11:03 IST 2020
 Description: 
 Main jetson/pc python file for controlling gimbal via the tracked object.
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Mon 27 Apr 18:11:03 IST 2020
"""

#import gimbalcmd

if __name__ == '__main__':
  import serial
  import time
  #import ball_tracking
  import cv2
  import ComArduino2
  #import 
  #import 


""" WRITE YOUR FUNCTIONS HERE """

def grab_function():
#  """
#  () -> ()
#  Description:Thread Running at 60 fps. T = 17MS. 
#  >>> 
#  
#  """


#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """


#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """

""" START YOUR CODE HERE """

if __name__ == '__main__':
  pass

  print
  print

  # waits until I receive a message Arduino ready from arduino setup part.
  # Obcomp should be ready first follwed by the duino.
  print("waiting for arduino response.")
  ComArduino2.waitForArduino()

  print("stm read successfully. LED should be blinking.")
  
  # creating an empty buffer list.
  gimbal_coords_buffer = []


  gimbal_coords_buffer.append("<100,200,0.2>")
  #gimbal_coords_buffer.append("<101,200,0.2>")
  #gimbal_coords_buffer.append("<102,200,0.2>")
  #gimbal_coords_buffer.append("<103,200,0.2>")
  #gimbal_coords_buffer.append("<104,200,0.2>")


  ComArduino2.runTest(gimbal_coords_buffer)
  

  #while (1):
  #      ball_tracking.live_tracking()
        #key = cv2.waitKey(1) & 0xFF
        #if key == ord("q"):
        #      break
        #ball_tracking.vs.stop()
        #cv2.destroyAllWindows()
  #import doctest
  #doctest.testmod()
  
  
  
  
""" END OF FILE """

