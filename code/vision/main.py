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
  import concurrent.futures
  import logging
  import queue
  import random
  import threading
  import serial
  import time
  #import ball_tracking
  import cv2
  #import ComArduino2
  #import 
  #import 

  imageQ = queue.Queue(maxsize=10)
  commQ = queue.Queue(maxsize=10)





""" WRITE YOUR FUNCTIONS HERE """

def grab_function():
#  """
#  () -> ()
#  Description:Thread Running at 60 fps. T = 17MS. 
#  >>> 
#  
#  """
  pass

#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """

def grabber_thread(event, source = 0, imgQ = imageQ):
    """
    (int, queue) -> NoneType
    Description : Grabs the image and puts it into the imageQ buffer.
    """
    cap = cv2.VideoCapture(source)
    lock = threading.Lock()
        
    while not event.is_set() or not imgQ.full():
        start_time = time.time() # start time of the loop
        logging.info(" no of frames"  + str(imgQ.qsize()))
        
        grabbed, frame = cap.read()
        
        lock.acquire()
        imgQ.put(frame)
        lock.release()
        logging.info("FPS frame grab: " + str(1.0 / (time.time() - start_time))) # FPS = 1 / time to process loop
    
    cap.stop()
    cap.release()


#def show_frame(frame, event):
#  while not event.is_set():


def process_thread(event, source = 0, trajQ = commQ, imgQ = imageQ):
  """
  @brief : pops imgQ process img and calc gimb trajectory.
  """
  while not event.is_set() or not queue.empty():
    start_time_proc = time.time()
    frame = imgQ.get()
    logging.info(" no of process frames"  + str(imgQ.qsize()))
    
    #if (source != 0):
    #  frame =  cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    #if frame is None:
    #  break
    #frame = imutils.resize(frame, width=600)
    #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    ## construct a mask for the color "green", then perform
    ## a series of dilations and erosions to remove any small
    ## blobs left in the mask
    #mask = cv2.inRange(hsv, greenLower, greenUpper)
    #mask = cv2.erode(mask, None, iterations=2)
    #mask = cv2.dilate(mask, None, iterations=2)
#
    #    # find contours in the mask and initialize the current
    ## (x, y) center of the ball
    #cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    #  cv2.CHAIN_APPROX_SIMPLE)
    #cnts = imutils.grab_contours(cnts)
    #center = None
    ## only proceed if at least one contour was found
    #if len(cnts) > 0:
    #  # find the largest contour in the mask, then use
    #  # it to compute the minimum enclosing circle and
    #  # centroid
    #  c = max(cnts, key=cv2.contourArea)
    #  ((x, y), radius) = cv2.minEnclosingCircle(c)
    #  M = cv2.moments(c)
    #  center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    #  # only proceed if the radius meets a minimum size
    #  if radius > 10:
    #    # draw the circle and centroid on the frame,
    #    # then update the list of tracked points
    #    cv2.circle(frame, (int(x), int(y)), int(radius),
    #      (0, 255, 255), 2)
    #    cv2.circle(frame, center, 5, (0, 0, 255), -1)
    ## update the points queue
    #pts.appendleft(center)
    ##print(center)
    #if((center) == None):
    #  center_message = "-1, -1, -1"
    #else:
    #  center_message = "100, " + str(center[0]) + ', ' + str(center[1])
#
    ## loop over the set of tracked points
    #for i in range(1, len(pts)):
    #  # if either of the tracked points are None, ignore
    #  # them
    #  if pts[i - 1] is None or pts[i] is None:
    #    continue
    #  # otherwise, compute the thickness of the line and
    #  # draw the connecting lines
    #  thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    #  cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    ## show the frame to our screen
    #cv2.imshow("Frame", frame)
    cv2.imshow("Process Frame", frame)
    if cv2.waitKey(10) == ord("q"):
      event.set()
      cv2.destroyAllWindows()
      break
    logging.info("FPS process : " + str(1.0 / (time.time() - start_time_proc))) # FPS = 1 / time to process loop
  
    #cv2.destroyAllWindows()
    #"""
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
  event = threading.Event()
    
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")



  #grab_th = threading.Thread(target = grabber_thread())
  #proc_th = threading.Thread(target = process_thread())
  #proc_th.start()
  #grab_th.start()
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(grabber_thread, event)
    executor.submit(process_thread, event)
   
  #  executor.submit(f2)
  
  #time.sleep(5.0)
  #event.set()
  # waits until I receive a message Arduino ready from arduino setup part.
  # Obcomp should be ready first follwed by the duino.
  #print("waiting for arduino response.")
  #ComArduino2.waitForArduino()
  #print("stm read successfully. LED should be blinking.")
  
  # creating an empty buffer list.
  #gimbal_coords_buffer = []


  #gimbal_coords_buffer.append("<100,200,0.2>")
  #gimbal_coords_buffer.append("<101,200,0.2>")
  #gimbal_coords_buffer.append("<102,200,0.2>")
  #gimbal_coords_buffer.append("<103,200,0.2>")
  #gimbal_coords_buffer.append("<104,200,0.2>")


  #ComArduino2.runTest(gimbal_coords_buffer)
  

  #while (1):
  #  if cv2.waitKey(1) == ord("q"):
  #    event.set()
  #    cv2.destroyAllWindows()
  #      ball_tracking.live_tracking()
        #key = cv2.waitKey(1) & 0xFF
        #if key == ord("q"):
        #      break
        #ball_tracking.vs.stop()
        #cv2.destroyAllWindows()
  #import doctest
  #doctest.testmod()
  
  
  
  
""" END OF FILE """

