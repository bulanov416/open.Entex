import cv2 as cv
import numpy as np
import sys

video = cv.VideoCapture('ptest.avi')

sys.setrecursionlimit(2000)
backgroundSubtractor = cv.createBackgroundSubtractorMOG2(varThreshold=100, detectShadows = True)

#Initializes video width and height
WIDTH = 0
HEIGHT = 0

#Total tallies of people entering and exiting
ENTER = 0
EXIT = 0

#People
people_in_frame = []

#Colors for drawing CV/UI
blue = np.array([255, 0, 0])
green = np.array([0, 255, 0])
red = np.array([0, 0, 255])
purple = np.array([128, 0, 128])
orange = np.array([0, 128, 255])
yellow = np.array([0, 255, 255])

#Recursive function detect if it is a person or noise
def island_size(scores, visited, rows, cols, i, j):
    visited[i, j] = True
    isl_size = 1

    if i - 1 >= 0 and scores[i-1, j] and not visited[i-1, j]:
        isl_size += island_size(scores, visited, rows, cols, i-1, j)
    if i + 1 < rows and scores[i+1, j] and not visited[i+1, j]:
        isl_size += island_size(scores, visited, rows, cols, i+1, j)
    if j - 1 >= 0 and scores[i, j-1] and not visited[i, j-1]:
        isl_size += island_size(scores, visited, rows, cols, i, j-1)
    if j + 1 < cols and scores[i, j+1] and not visited[i, j+1]:
        isl_size += island_size(scores, visited, rows, cols, i, j+1)

    return isl_size

# GIVES ALL THE ISLAND INFO. Size, mean, etc.
def get_orange_island(scores, visited, rows, cols, i, j, step):

    orange_island = {
        "size": 1,
        "x-coords": [i * step],
        "y-coords": [j * step]
    }

    def update_oi (o_i):
        orange_island["size"] += o_i["size"]
        orange_island["x-coords"] += o_i["x-coords"]
        orange_island["y-coords"] += o_i["y-coords"]

    visited[i, j] = True

    if i - 1 >= 0 and scores[i-1, j] and not visited[i-1, j]:
        update_oi(get_orange_island(scores, visited, rows, cols, i-1, j, step))
    if i + 1 < rows and scores[i+1, j] and not visited[i+1, j]:
        update_oi(get_orange_island(scores, visited, rows, cols, i+1, j, step))
    if j - 1 >= 0 and scores[i, j-1] and not visited[i, j-1]:
        update_oi(get_orange_island(scores, visited, rows, cols, i, j-1, step))
    if j + 1 < cols and scores[i, j+1] and not visited[i, j+1]:
        update_oi(get_orange_island(scores, visited, rows, cols, i, j+1, step))

    return orange_island

class Person:
    def __init__(self, x, y, movement):
        self.x_history = [x]
        self.y_history = [y]
        self.movement = 0;
        #self.color = np.array([np.random.randint(50, 255), np.random.randint(50, 255), np.random.randint(50, 255)])

def str_oi(oi):
    return str(oi["x-mean"]) + ':' + str(oi["y-mean"])

def bounding_boxes(fgmask, frame, box_w, box_h, step, threshold, isl_threshold):
    global ENTER, EXIT, people_in_frame

    scores_rows = (WIDTH - box_w) // step + 1
    scores_cols = (HEIGHT - box_h) // step + 1

    scores = np.empty(shape=(scores_rows, scores_cols))

    for i in range(0, WIDTH - box_w, step):
        for j in range(0, HEIGHT - box_h, step):
            scores[i // step, j // step] = np.sum(fgmask[j:j+box_h, i:i+box_w]) / (box_w * box_h * 255)

    visited = np.zeros(np.shape(scores), dtype = bool)
    scores = scores > threshold

    num_people = 0

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
        orange_island["x-mean"] = int(np.mean(orange_island["x-coords"]))
        orange_island["y-mean"] = int(np.mean(orange_island["y-coords"]))
        #for x, y in zip(orange_island["x-coords"], orange_island["y-coords"]):
            #frame[y:y+step, x:x+step] = green

    CLOSENESS_THRESHOLD = 200
    new_people_in_frame = []
    matched_orange_islands = set()

    for person in people_in_frame:
        for orange_island in orange_islands:
            ox = orange_island["x-mean"]
            oy = orange_island["y-mean"]
            if np.sqrt((ox - person.x_history[-1]) ** 2 + (oy - person.y_history[-1]) ** 2) <= CLOSENESS_THRESHOLD:
                person.x_history.append(ox)
                person.y_history.append(oy)
                new_people_in_frame.append(person)
                matched_orange_islands.add(str_oi(orange_island))
                break

    for orange_island in orange_islands:
        if str_oi(orange_island) not in matched_orange_islands:
            new_people_in_frame.append(Person(orange_island["x-mean"], orange_island["y-mean"], 0))

    people_in_frame = new_people_in_frame
    for person in people_in_frame:
        if len(person.x_history) > 5:
            x = person.x_history
            x1 = x[-1]
            x5 = x[-5]
            if x1 > WIDTH//2 and x5 < WIDTH//2 and person.movement == 0:
                print(x1, x5)
                EXIT += 1
                person.movement = -1
            if x1 < WIDTH//2 and x5 > WIDTH//2 and person.movement == 0:
                print(x1, x5)
                ENTER += 1
                person.movement = 1
            if x1 > 3*WIDTH//4 or x1 < WIDTH//4:
                person.movement = 0
    #PURPLE BAR
    frame[0:16, 0:WIDTH//2] = purple
    frame[HEIGHT-16:HEIGHT, 0:WIDTH//2] = purple
    frame[0:HEIGHT, WIDTH//2-8:WIDTH//2+8] = purple
    frame[HEIGHT-200:HEIGHT - 30, WIDTH//2-125:WIDTH//2 + 300] = purple
    """
    for person in people_in_frame:
        x_history = person.x_history
        y_history = person.y_history
        for k in range(len(x_history) - 10, len(x_history)):
            if k >= 0:
                frame[y_history[k]-8:y_history[k]+8, x_history[k]-8:x_history[k]+8] = person.color
        frame[y_history[-1]-16:y_history[-1]+16, x_history[-1]-16:x_history[-1]+16] = blue
    """
    return { "people": people_in_frame }

while True:
    ret, frame = video.read()

    fgmask = backgroundSubtractor.apply(frame)
    HEIGHT = fgmask.shape[0]
    WIDTH = fgmask.shape[1]

    backtorgb = cv.cvtColor(fgmask, cv.COLOR_GRAY2RGB)
    box_info = bounding_boxes(fgmask, frame, 32, 32, 32, 0.4, 40)
    box_text = f"Visible People: {len(box_info['people'])}"

    # font
    font = cv.FONT_HERSHEY_SIMPLEX
    fontScale = 1.5
    thickness = 4

    # Using cv2.putText() method
    frame = cv.putText(frame, box_text, (WIDTH*4//9, HEIGHT - 150), font,
                       fontScale, (255, 255, 255), thickness, cv.LINE_AA)
    frame = cv.putText(frame, ('Entered: ' + str(ENTER)), (WIDTH*4//9, HEIGHT - 100), font,
                       fontScale, (255, 255, 255), thickness, cv.LINE_AA)
    frame = cv.putText(frame, ('Left: ' + str(EXIT)), (WIDTH*4//9, HEIGHT - 50), font,
                       fontScale, (255, 255, 255), thickness, cv.LINE_AA)

    frame = cv.putText(frame, ('INSIDE: ' + str(ENTER - EXIT)), (WIDTH*1//6, 150), font,
        2*fontScale, (255, 255, 255), 4*thickness, cv.LINE_AA)
    frame = cv.putText(frame, ('OUTSIDE'), (WIDTH*4//6, 150), font,
        2*fontScale, (255, 255, 255), 4*thickness, cv.LINE_AA)
    cv.imshow('frame', frame)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

video.release()
cv.destroyAllWindows()
