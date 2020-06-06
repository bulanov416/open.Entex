import cv2
import numpy as np

# Video available at https://www.youtube.com/watch?v=RQgn1m9cP8g

cap = cv2.VideoCapture('vtest.avi')


"""
DON'T FORGET TO TINKER WITH SETTINGS FOR BETTER BACKGROUND DETECTION!
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_video/py_bg_subtraction/py_bg_subtraction.html#background-subtraction
"""
fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=80, detectShadows = True)

WIDTH = 640
HEIGHT = 360
green = np.array([0, 255, 0])

def green_rect(frame, x, y, w, h):
    frame[y:y + h, x] = green
    frame[y:y + h, x + w - 1] = green
    frame[y, x:x + w] = green
    frame[y + h, x:x + w - 1] = green

def bounding_boxes(fgmask, frame, box_w, box_h, step, threshold):
    # scores is a matrix containing values 0 <= x <= 1.
    # 0 indicates a completely black area and 1 indicates
    # a completely white area.
    scores_rows = (WIDTH - box_w) // step + 1
    scores_cols = (HEIGHT - box_h) // step + 1
    scores = np.empty(shape=(scores_rows, scores_cols))
    for i in range(0, WIDTH - box_w, step):
        for j in range(0, HEIGHT - box_h, step):
            scores[i // step, j // step] = np.sum(fgmask[j:j+box_h, i:i+box_w]) / (box_w * box_h * 255)

    for i in range(scores_rows - 1):
        for j in range(scores_cols - 1):
            score = scores[i, j]
            if score >= threshold:
                green_rect(frame, i * step, j * step, box_w, box_h)


while True:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    backtorgb = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2RGB)

    bounding_boxes(fgmask, frame, 8, 8, 8, 0.4)

    cv2.imshow('frame', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
