import numpy as np
import matplotlib.pyplot as plt

import cv2
def detect_qr_code(image):

    qrCodeDetector = cv2.QRCodeDetector()

    decodedText, points, _ = qrCodeDetector.detectAndDecode(image)
    points =np.array(points)
    if points is not None and points.size>1:
        print(points.size)
        nrOfPoints = len(points)

        for i in range(nrOfPoints):
            nextPointIndex = (i + 1) % nrOfPoints
            point= tuple(points[i][0].astype(int))
            cv2.line(image, tuple(points[i][0].astype(int)), tuple(points[nextPointIndex][0].astype(int)), (255, 0, 255), 15)

        print(decodedText)

        return image , point


    else:
        print("QR code not detected")
        return image




def show(img1, img2 ,img3 ,img4 ,img5 ,img6) :
    plt.subplot(3, 2, 1), plt.imshow(img1, cmap="gray"), plt.title('detect left corner')
    plt.xticks([]), plt.yticks([])
    plt.subplot(3, 2, 2), plt.imshow(img2, cmap="gray"), plt.title('detect left corner')
    plt.xticks([]), plt.yticks([])
    plt.subplot(3, 2, 3), plt.imshow(img3, cmap="gray"), plt.title('detect left corner')
    plt.xticks([]), plt.yticks([])
    plt.subplot(3, 2, 4), plt.imshow(img4, cmap="gray"), plt.title('detect left corner')
    plt.xticks([]), plt.yticks([])
    plt.subplot(3, 2, 5), plt.imshow(img5, cmap="gray"), plt.title('detect left corner')
    plt.xticks([]), plt.yticks([])
    plt.subplot(3, 2, 6), plt.imshow(img6, cmap="gray"), plt.title('detect left corner')
    plt.xticks([]), plt.yticks([])
    plt.savefig('./test_qr_code/results.jpg')
    plt.show()


if __name__ == '__main__':
    img1 = cv2.imread('test_qr_code/1.jpg')
    img2 = cv2.imread('test_qr_code/2.jpg')
    img3 = cv2.imread('test_qr_code/3.jpg')
    img4 = cv2.imread('test_qr_code/4.jpg')
    img5 = cv2.imread('test_qr_code/5.jpg')
    img6 = cv2.imread('test_qr_code/6.jpg')
    img1 , point1 = detect_qr_code(img1)
    img2 ,point2 = detect_qr_code(img2)
    img3 ,point3 = detect_qr_code(img3)
    img4 ,point4= detect_qr_code(img4)
    img5, point5= detect_qr_code(img5)
    img6, point6 = detect_qr_code(img6)
    print(point1)
    print(point2)
    print(point3)
    print(point4)
    print(point5)
    print(point6)

    show(img1,img2,img3,img4,img5,img6)
