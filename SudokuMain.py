import cv2
import numpy as np
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#####################################################
def splitBoxes(img):
    rows = np.vsplit(img, 9)
    boxes = []
    for i in range(len(rows)):
        cols = np.hsplit(rows[i], 9)
        boxes.append([])
        for box in cols:
            boxes[i].append(box)
    return boxes

#####################################################
def getdigit(boxes):
    res = []
    for i in range(len(boxes)):
        res.append([])
        for j in range(len(boxes[i])):
            temp = tess.image_to_boxes(boxes[i][j][10:, 10:], config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
            if len(temp) > 0:
                res[i].append(int(temp[0]))
            else:
                res[i].append(0)
    return res

#####################################################
def getBlankPos(mainGame):
    res = []
    for i in range(len(mainGame)):
        for j in range(len(mainGame[i])):
            if mainGame[i][j] == 0:
                res.append(i*9+j)
    return res

#####################################################
def possible(x, y, val):
    for i in range(9):
        if mainGame[i][y] == val or mainGame[x][i] == val:
            return False
    (startX, startY, endX, endY) = (0, 0, 2, 2) 
    if x >= 3 and x <= 5:
        ( startX, endX ) = (3, 5)
    elif x > 5:
        ( startX, endX ) = (6, 8)

    if y >= 3 and y <= 5:
        ( startY, endY ) = (3, 5)
    elif y > 5:
        ( startY, endY ) = (6, 8)

    for i in range(startX, endX + 1):
        for j in range(startY, endY + 1):
            if mainGame[i][j] == val:
                return False
    
    return True
#####################################################
def sudokuSolver(cur):
    if cur >= len(blank):
        return True
    x = blank[cur]//9
    y = blank[cur]%9
    for i in range(1, 10):
        if possible(x, y, i):
            mainGame[x][y] = i
            #print(x, y, i)
            if sudokuSolver(cur+1):
                return True
            mainGame[x][y] = 0

#####################################################
def printResult(img):
    for i in blank:
        y = i//9
        x = i%9
        cv2.putText(img, str(mainGame[y][x]), (x*size+20,y*size+50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    return img

#####################################################
img = cv2.imread("A.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (630, 630))
size = 70
'''
img = cv2.Canny(img, 100, 200)
img = cv2.adaptiveThreshold(img, 255, 1, 1, 3, 3)
'''
boxes = splitBoxes(img)

mainGame = getdigit(boxes)
blank = getBlankPos(mainGame)
sudokuSolver(0)
img = printResult(img)
#b = tess.image_to_string(boxes[3][0], config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
cv2.imshow("Result", img)
cv2.waitKey(0)
