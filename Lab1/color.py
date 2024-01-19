import numpy as np
import cv2
from sklearn.cluster import KMeans

"""
Citations:
Video display   https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
Bounding box    https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html
Dominant Color  https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097

"""

cap = cv2.VideoCapture(0)
clt = KMeans(n_clusters = 1) # cluster number

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Establish rectangle to capture dominant color
    cv2.rectangle(frame, (280, 200), (360, 280), (0,255,0), 2)
    # Run K-Means on pixels within rectange
    sampleImg = rgb[200:280, 280:360]
    sampleImg = sampleImg.reshape((sampleImg.shape[0] * sampleImg.shape[1], 3)) #represent as row*column,channel number
    clt.fit(sampleImg)
    #Get dominantColor and creat image with that color
    dominantColor = clt.cluster_centers_
    blank_image = np.zeros((300, 300, 3), np.uint8)
    blank_image[:,:,:] = dominantColor
    blank_image = cv2. cvtColor(blank_image, cv2.COLOR_RGB2BGR)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('dominant color', blank_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()