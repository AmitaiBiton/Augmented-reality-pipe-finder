import numpy as np
import matplotlib.pyplot as plt

import cv2
def detect_qr_code(image):
    qrCodeDetector = cv2.QRCodeDetector()
    point_list = []
    decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
    points =np.array(points)
    if points is not None and points.size>1:
        nrOfPoints = len(points)

        for i in range(nrOfPoints):
            nextPointIndex = (i + 1) % nrOfPoints
            cv2.line(image, tuple(points[i][0].astype(int)), tuple(points[nextPointIndex][0].astype(int)), (255, 0, 255), 15)

        point_list.append(tuple(points[nextPointIndex][0].astype(int)))
        return image , point_list


    else:
        print("QR code not detected")
        return image




def show(img1, img2 ) :
    plt.subplot(2, 2, 1), plt.imshow(img1, cmap="gray"), plt.title('detect left corner')
    plt.xticks([]), plt.yticks([])
    plt.subplot(2, 2, 2), plt.imshow(img2, cmap="gray"), plt.title('detect left corner')
    plt.xticks([]), plt.yticks([])

    plt.savefig('./test_qr_code/results.jpg')
    plt.show()

"""
if __name__ == '__main__':
    img1 = cv2.imread('output/new5.jpg')

    img2 = cv2.imread('output_2/new5.jpg')

    img1 , point1 = detect_qr_code(img1)
    img2 ,point2 = detect_qr_code(img2)

    show(img1,img2)
"""
"""
import cv2
import numpy as np

# Load imgae, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread('./pipe_finder/salon/2.jpg')
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9,9), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Morph close
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# Find contours and filter for QR code
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    x,y,w,h = cv2.boundingRect(approx)
    area = cv2.contourArea(c)
    ar = w / float(h)
    if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
        ROI = original[y:y+h, x:x+w]
        cv2.imwrite('ROI.png', ROI)

cv2.imshow('thresh', thresh)
cv2.imshow('close', close)
cv2.imshow('image', image)

cv2.waitKey()
"""
import cv2
import numpy as np
def find_point (path):
    # Load imgae, grayscale, Gaussian blur, Otsu's threshold
    image = cv2.imread(path)
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph close
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours and filter for QR code
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)

        area = cv2.contourArea(c)
        ar = w / float(h)
        if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
            ROI = original[y:y+h, x:x+w]
            cv2.imwrite('ROI.png', ROI)

            return [[x,y],[x+w,y],[x,y+h] , [x+w,y+h]]


