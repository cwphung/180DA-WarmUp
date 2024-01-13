import numpy as np
import cv2
"""
Citations:
Video display   https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
Bounding box    https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html

"""
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerGreenHsv = np.array([50, 50, 50])
    upperGreenHsv = np.array([70, 255, 255])
    mask = cv2.inRange(hsvFrame, lowerGreenHsv, upperGreenHsv)

    # Draw bounding box around largest contour
    contours, hierarchy = cv2.findContours(mask, 1, 2)
    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()