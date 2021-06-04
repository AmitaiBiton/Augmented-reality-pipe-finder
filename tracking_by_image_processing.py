
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage


class LineTracking():

    def __init__(self,img_file):
        """The constructor."""
        """Read image from path file """
        self.img = cv2.imread(img_file)
        """some temp """
        self.img_inter = self.img
        """final image with the pipe detection """
        self.img_final = self.img
        """list of coordinate """
        self.cendroids = []
        self.mean_centroids = [0,0]

    def processing(self):
        plt.imshow(self.img)
        plt.show()
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        """clean image"""
        blur = cv2.GaussianBlur(gray,(5,5),0)
        """threah hold for the pipe agent's the well """
        ret,thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)


        plt.show()
        """opening and closing to remove the noise for pipe and the well"""
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_close)

        connectivity = 8
        """
            thresh is what we gt still here now we want to points on the object we detected by thresh 
            so in the output we get the labels and the coordinates of the object 
        """
        output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)

        num_labels = output[0]
        labels = output[1]
        stats = output[2]
        print(output[3] , output[0])
        self.centroids = output[3]
        """
        for c in self.centroids :

            self.mean_centroids[0] += c[0]/len(self.centroids)
            self.mean_centroids[1] += c[1]/len(self.centroids)
        """
        self.img_final = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        for c in self.centroids :
            self.img_final[int(c[1])-5 : int(c[1])+10, int(c[0])-5 : int(c[0])+10] = [0,255,0]

    def remove_small_objects(img, min_size=150):
        # find all your connected components (white blobs in your image)
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
        # connectedComponentswithStats yields every seperated component with information on each of them, such as size
        # the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
        sizes = stats[1:, -1]
        nb_components = nb_components - 1

        # your answer image
        img2 = img
        # for every component in the image, you keep it only if it's above min_size
        for i in range(0, nb_components):
            if sizes[i] < min_size:
                img2[output == i + 1] = 0

        return img2

if __name__ == '__main__':
    test = LineTracking('./output/newimage.jpg')
    img = np.copy(test)
    test.processing()
    print(type(test.img))
    plt.imshow(test.img_final)
    plt.show()
    img = cv2.imread('./output/newimage.jpg')
    """
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    lower = np.uint8([0, 100, 0])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)
    # yellow color mask
    lower = np.uint8([10, 0,   100])
    upper = np.uint8([40, 255, 255])
    yellow_mask = cv2.inRange(image, lower, upper)
    # combine the mask
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    result = img.copy()
    plt.imshow(mask)
    plt.show()
    """