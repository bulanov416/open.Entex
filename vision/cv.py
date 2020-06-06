import cv2
import numpy as np

import sys
sys.setrecursionlimit(2000)
# Video available at https://www.youtube.com/watch?v=RQgn1m9cP8g

cap = cv2.VideoCapture('ptest.avi')

fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=100, detectShadows = True)

WIDTH = 640
HEIGHT = 360
green = np.array([0, 255, 0])
red = np.array([0, 0, 255])
yellah = np.array([0, 128, 255])
xcord = []
ycord = []

def green_rect(frame, x, y, w, h, thicc):
    if x - thicc < 0 or y - thicc < 0 or x + w >= WIDTH or y + h >= HEIGHT:
        return
    frame[y:y + h, x-thicc:x] = green
    frame[y:y + h, x+w-thicc:x+w-1] = green
    frame[y-thicc:y, x:x + w] = green
    #print(y + h, HEIGHT)
    frame[y+h-thicc:y+h, x:x+w-1] = green

def island_size(scores, vted, rows, cols, i, j):
    vted[i, j] = True
    isl_size = 1
    if i - 1 >= 0 and scores[i-1, j] and not vted[i-1, j]:
        isl_size += island_size(scores, vted, rows, cols, i-1, j)
    if i + 1 < rows and scores[i+1, j] and not vted[i+1, j]:
        isl_size += island_size(scores, vted, rows, cols, i+1, j)
    if j - 1 >= 0 and scores[i, j-1] and not vted[i, j-1]:
        isl_size += island_size(scores, vted, rows, cols, i, j-1)
    if j + 1 < cols and scores[i, j+1] and not vted[i, j+1]:
        isl_size += island_size(scores, vted, rows, cols, i, j+1)
    return isl_size

"""
def falsify(scores, rows, cols, i, j):
    scores[i, j] = 0
    if i - 1 >= 0 and scores[i-1, j]:
        falsify(scores, rows, cols, i-1, j)
    if i + 1 < rows and scores[i+1, j]:
        falsify(scores, rows, cols, i+1, j)
    if j - 1 >= 0 and scores[i, j-1]:
        falsify(scores, rows, cols, i, j-1)
    if j + 1 < cols and scores[i, j+1]:
        falsify(scores, rows, cols, i, j+1)
"""

def bounding_boxes(fgmask, frame, box_w, box_h, step, threshold, isl_threshold):
    global xcord
    global ycord
    # scores is a matrix containing values 0 <= x <= 1.
    # 0 indicates a completely black area and 1 indicates
    # a completely white area.
    scores_rows = (WIDTH - box_w) // step + 1
    scores_cols = (HEIGHT - box_h) // step + 1
    scores = np.empty(shape=(scores_rows, scores_cols))
    for i in range(0, WIDTH - box_w, step):
        for j in range(0, HEIGHT - box_h, step):
            scores[i // step, j // step] = np.sum(fgmask[j:j+box_h, i:i+box_w]) / (box_w * box_h * 255)


    THICC = 3

    visited = np.zeros(np.shape(scores), dtype = bool)
    scores = scores > threshold
    #print(visited)

    num_people = 0
    """
    for i in range(scores_rows - 1):
        
        for j in range(scores_cols - 1):
            isl_size = island_size(scores, visited, scores_rows, scores_cols, i, j)

            if isl_size >= isl_threshold:
                for x, y in zip(xcord, ycord):
                    frame[y*step:(y+1)*step, x*step:(x+1)*step] = yellah

                xmean = np.sum(np.array(xcord))//len(xcord)*step
                ymean = np.sum(np.array(ycord))//len(ycord)*step
                frame[ymean-8:ymean+8, xmean-8:xmean+8] = red
                ycord = []
                xcord = []
                num_people += 1
            print(isl_size)
    """

    for i in range(scores_rows - 1):
        for j in range(scores_cols - 1):
            score = scores[i, j]
            x = i * step
            y = j * step
            if score:# >= threshold:
                xcord.append(x)
                ycord.append(y)
                frame[y:y+step, x:x+step] = green
                """
                # Left edge
                if x - THICC >= 0 and scores[i - 1, j] < threshold:
                    frame[y:y+step, x-THICC:x] = green
                # Right edge
                if x + step < WIDTH and scores[i + 1, j] < threshold:
                    frame[y:y+step, x+step-THICC:x+step-1] = green
                # Top
                if y - THICC >= 0 and scores[i, j - 1] < threshold:
                    frame[y-THICC:y, x:x+step] = green
                # Bottom
                if y + step < HEIGHT and scores[i, j + 1] < threshold:
                    frame[y+step-THICC:y+step, x:x+step-1] = green
                """
    if len(xcord) != 0 and len(ycord) != 0:
        xmean = int(np.sum(np.array(xcord))//len(xcord))
        ymean = int(np.sum(np.array(ycord))//len(ycord))
        frame[ymean-4:ymean+4, xmean-4:xmean+4] = red
        print(xmean, ymean)
    ycord = []
    xcord = []


frame_count = 0
while True:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    HEIGHT = fgmask.shape[0]
    WIDTH = fgmask.shape[1]

    backtorgb = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2RGB)

    bounding_boxes(fgmask, backtorgb, 32, 32, 32, 0.4, 25)

    cv2.imshow('frame', backtorgb)
    k = cv2.waitKey(30) & 0xff
    frame_count += 1
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()