import cv2
from PIL import Image
import time
import numpy as np
import cv2


def find_limit(color):

    c=np.uint8([[color]]) #bgr to hsv
    hsvc=cv2.cvtColor(c,cv2.COLOR_BGR2HSV)

    lowerLimit=hsvc[0][0][0]-10,100,100
    upperLimit=hsvc[0][0][0]+10,255,255

    lowerLimit=np.array(lowerLimit,dtype=np.uint8)
    upperLimit=np.array(upperLimit,dtype=np.uint8)

    return lowerLimit,upperLimit


yellow = [0, 255, 255]
cap = cv2.VideoCapture(0)

# Variables for FPS calculation
prev_time = 0
fps = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ---- FPS Calculation ----
    current_time = time.time()
    if prev_time != 0:
        fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # ---- Color detection ----
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    llimit, ulimit = find_limit(yellow)
    mask = cv2.inRange(hsvImage, llimit, ulimit)

    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    # ---- Display FPS on frame ----
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # ---- Show frame ----
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
