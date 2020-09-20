import cv2
import numpy as np
from goprocam import GoProCamera
from goprocam import constants
cascPath="../env-oscar/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_default.xml"
gpCam = GoProCamera.GoPro()
#gpCam.gpControlSet(constants.Stream.BIT_RATE, constants.Stream.BitRate.B2_4Mbps)
#gpCam.gpControlSet(constants.Stream.WINDOW_SIZE, constants.Stream.WindowSize.W480)
cap = cv2.VideoCapture("udp://127.0.0.1:10000")
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Display the resulting frame
    #frame =  cv2.rotate(frame, cv2.ROTATE_180)
    cv2.imshow("GoPro OpenCV", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()