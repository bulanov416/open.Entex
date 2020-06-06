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
objectPath = []

#Colors
blue = np.array([255, 0, 0])
green = np.array([0, 255, 0])
red = np.array([0, 0, 255])
orange = np.array([0, 128, 255])
yellow = np.array([0, 255, 255])

#Recursive function detect if it is a person or noise
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

# GIVES ALL THE ISLAND INFO. Size, mean, etc.
def get_orange_island(scores, vted, rows, cols, i, j, step):
    vted[i, j] = True
    orange_island = {
        "size": 1,
        "x-coords": [i * step],
        "y-coords": [j * step]
    }
    if i - 1 >= 0 and scores[i-1, j] and not vted[i-1, j]:
        o_i = get_orange_island(scores, vted, rows, cols, i-1, j, step)
        orange_island["size"] += o_i["size"]
        orange_island["x-coords"] += o_i["x-coords"]
        orange_island["y-coords"] += o_i["y-coords"]
    # Important to have rows-1
    if i + 1 < rows - 1 and scores[i+1, j] and not vted[i+1, j]:
        o_i = get_orange_island(scores, vted, rows, cols, i+1, j, step)
        orange_island["size"] += o_i["size"]
        orange_island["x-coords"] += o_i["x-coords"]
        orange_island["y-coords"] += o_i["y-coords"]
    if j - 1 >= 0 and scores[i, j-1] and not vted[i, j-1]:
        o_i = get_orange_island(scores, vted, rows, cols, i, j-1, step)
        orange_island["size"] += o_i["size"]
        orange_island["x-coords"] += o_i["x-coords"]
        orange_island["y-coords"] += o_i["y-coords"]
    if j + 1 < cols and scores[i, j+1] and not vted[i, j+1]:
        o_i = get_orange_island(scores, vted, rows, cols, i, j+1, step)
        orange_island["size"] += o_i["size"]
        orange_island["x-coords"] += o_i["x-coords"]
        orange_island["y-coords"] += o_i["y-coords"]
    return orange_island

def bounding_boxes(fgmask, frame, box_w, box_h, step, threshold, isl_threshold):
    global xcord
    global ycord

    scores_rows = (WIDTH - box_w) // step + 1
    scores_cols = (HEIGHT - box_h) // step + 1

    scores = np.empty(shape=(scores_rows, scores_cols))

    for i in range(0, WIDTH - box_w, step):
        for j in range(0, HEIGHT - box_h, step):
            scores[i // step, j // step] = np.sum(fgmask[j:j+box_h, i:i+box_w]) / (box_w * box_h * 255)

    THICC = 3
    visited = np.zeros(np.shape(scores), dtype = bool)
    scores = scores > threshold

    num_people = 0
    for i in range(scores_rows - 1):
        for j in range(scores_cols):
            score = scores[i, j]
            x = i * step
            y = j * step
            if score:
                xcord.append(x)
                ycord.append(y)
                frame[y:y+step, x:x+step] = yellow
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

    # Build list of orange islands
    orange_visited = np.zeros(shape=scores.shape, dtype=bool)
    orange_islands = []
    for i in range(scores_rows - 1):
        for j in range(scores_cols):
            if scores[i, j] and not orange_visited[i, j]:
                orange_island = get_orange_island(scores, orange_visited, scores_rows, scores_cols, i, j, step)
                if orange_island["size"] >= isl_threshold:
                    orange_islands.append(orange_island)

    for orange_island in orange_islands:
        # Retrieve island properties
        x_coords = orange_island["x-coords"]
        y_coords = orange_island["y-coords"]
        x_mean = int(np.mean(x_coords))
        y_mean = int(np.mean(y_coords))
        for x, y in zip(x_coords, y_coords):
            frame[y:y+step, x:x+step] = orange
        objectPath.append([x_mean, y_mean])
        for k in range(len(objectPath) - 10, len(objectPath)):
            if k >= 0:
                frame[objectPath[k][1]-4:objectPath[k][1]+4, objectPath[k][0]-4:objectPath[k][0]+4] = red
        frame[y_mean-16:y_mean+16, x_mean-16:x_mean+16] = blue

    """
    if len(xcord) != 0 and len(ycord) != 0:
        xmean = int(np.sum(np.array(xcord))//len(xcord))
        ymean = int(np.sum(np.array(ycord))//len(ycord))
        frame[ymean-4:ymean+4, xmean-4:xmean+4] = red
        print(xmean, ymean)
    ycord = []
    xcord = []
    """
    return {
        "people": orange_islands
    }

while True:
    ret, frame = video.read()

    fgmask = fgbg.apply(frame)
    HEIGHT = fgmask.shape[0]
    WIDTH = fgmask.shape[1]

    backtorgb = cv.cvtColor(fgmask, cv.COLOR_GRAY2RGB)

    box_info = bounding_boxes(fgmask, frame, 32, 32, 32, 0.4, 40)

    box_text = f"Number of People: {len(box_info['people'])}"

    # font 
    font = cv.FONT_HERSHEY_SIMPLEX 
  
    # org 
    org = (50, 50) 
      
    # fontScale 
    fontScale = 1
      
    # Line thickness of 2 px 
    thickness = 2
       
    # Using cv2.putText() method 
    frame = cv.putText(frame, box_text, org, font,  
                       fontScale, (255, 255, 255), thickness, cv.LINE_AA)

    cv.imshow('frame', frame)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

video.release()
cv.destroyAllWindows()
