import cv2 as cv
import numpy as np
import sys

video = cv.VideoCapture('ptest.avi')

sys.setrecursionlimit(2000)
fgbg = cv.createBackgroundSubtractorMOG2(varThreshold=100, detectShadows = True)

#Initializes width and height
WIDTH = 0
HEIGHT = 0

#Initializes arrays for object tracking
xcord = []
ycord = []

#Colors
green = np.array([0, 255, 0])
red = np.array([0, 0, 255])
orange = np.array([0, 128, 255])

"""
def outlined_rect(frame, x, y, w, h, thick, color):
    #Edge cases
    if x - thick < 0 or y - thick < 0 or x + w >= WIDTH or y + h >= HEIGHT:
        return

    #Draws Each Border
    frame[y:y + h, x-thick:x] = color
    frame[y:y + h, x+w-thick:x+w-1] = color
    frame[y-thick:y, x:x + w] = color
    frame[y+h-thick:y+h, x:x+w-1] = color
"""

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
                    frame[y*step:(y+1)*step, x*step:(x+1)*step] = orange

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
    ret, frame = video.read()

    fgmask = fgbg.apply(frame)
    HEIGHT = fgmask.shape[0]
    WIDTH = fgmask.shape[1]

    backtorgb = cv.cvtColor(fgmask, cv.COLOR_GRAY2RGB)

    bounding_boxes(fgmask, backtorgb, 32, 32, 32, 0.4, 25)

    cv.imshow('frame', backtorgb)
    k = cv.waitKey(30) & 0xff
    frame_count += 1
    if k == 27:
        break

video.release()
cv.destroyAllWindows()
