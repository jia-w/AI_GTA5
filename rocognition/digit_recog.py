import cv2
import os
import numpy as np
from PIL import Image

def getDataSet():
    img = cv2.imread('C:/Users/pc/Desktop/recog/digit.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cells = [np.hsplit(row,9) for row in np.vsplit(gray,10)]
    x = np.array(cells)
    train = x[:,:].reshape(-1,90).astype(np.float32)

    k = np.arange(10)
    train_labels = np.repeat(k,10)[:,np.newaxis]

    np.savez('C:/Users/pc/Desktop/recog/digit.npz',train=train,train_labels = train_labels)


def loadTrainData(fname):
    with np.load(fname) as data:
        train = data['train']
        train_labels = data['train_labels']

    return train, train_labels

def checkDigit(test, train, train_labels):
    knn = cv2.ml.KNearest_create()
    knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)
    ret, result, neighbours, dist = knn.findNearest(test, k=1)

    return result

def resize9x10(digit_img):
  # img = cv2.imread(digit_img)
    gray = cv2.cvtColor(digit_img, cv2.COLOR_BGR2GRAY)
    ret = cv2.resize(gray, (9,10), fx=1, fy=1, interpolation=cv2.INTER_AREA)
    ret, thr = cv2.threshold(gray, 180, 255,cv2.THRESH_BINARY)
    #cv2.imshow('num',thr)
    #cv2.waitKey(0)
    return thr.reshape(-1, 90).astype(np.float32)

def return_num(result):
    if result == 1: return 1
    elif result ==2: return 2
    elif result ==3: return 3
    elif result ==4: return 4
    elif result ==5: return 5
    elif result ==6: return 6
    elif result ==7: return 7
    elif result ==8: return 8
    elif result ==9: return 9
    elif result ==0: return 0
    elif ~(10 > result and result > -1): return ""

def digit_recog(path):
    cov_digit ='digit.npz'
    train, train_labels  = loadTrainData(cov_digit)

    savenpz = False
  
    #game screen shot path(only change this part)
    test_img = cv2.imread(path)

    num1 = test_img[572:582,680:689]
    num2 = test_img[572:582,688:697]
    num3 = test_img[572:582,695:704]
    '''
    area2 = (680,572,689,582)
    area3 = (688,572,697,582)
    area1 = (695,572,704,582)
    '''

    #crop the speed & check digit
    test = resize9x10(num1)
    test2 = resize9x10(num2)
    test3 = resize9x10(num3)

    result = checkDigit(test, train, train_labels)
    result2 = checkDigit(test2, train, train_labels)
    result3 = checkDigit(test3, train, train_labels)
        
    speed = ""
    #speed first digit
    if result >= 0 and result <= 9:
        speed += str(return_num(result))

    #speed second digit
    if (result >= 0 and result <= 9):
        speed += str(return_num(result2))
    #speed third digit
    if (result >= 0 and result <= 9):
        speed += str(return_num(result3))
        
    #speed
    return int(speed)


#return speed(int) , Use 800x600 screenshot
#print(digit_recog('C:/Users/pc/Documents/GomPlayer/Capture/GTA5_4.png'))