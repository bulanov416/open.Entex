import cv2

# Video available at https://www.youtube.com/watch?v=RQgn1m9cP8g

cap = cv2.VideoCapture('vtest.avi')


"""
DON'T FORGET TO TINKER WITH SETTINGS FOR BETTER BACKGROUND DETECTION!

https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html#background-subtraction
"""
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=32)

while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
