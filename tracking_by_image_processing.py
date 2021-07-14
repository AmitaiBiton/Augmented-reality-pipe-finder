import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage


class LineTracking():

    def __init__(self,img):
        """The constructor."""
        """Read image from path file """
        self.img = img
        """some temp """
        self.img_inter = self.img
        """final image with the pipe detection """
        self.img_final = self.img
        """list of coordinate """
        self.cendroids = []
        self.mean_centroids = [0,0]

    def processing(self):

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        """clean image"""
        blur = cv2.GaussianBlur(gray,(5,5),0)
        """threah hold for the pipe agent's the well """
        ret,thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY_INV)


        #plt.show()
        """opening and closing to remove the noise for pipe and the well"""
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open)
        self.img_final = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_close)
        self.img_final = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        """
        connectivity = 8
      
            thresh is what we gt still here now we want to points on the object we detected by thresh 
            so in the output we get the labels and the coordinates of the object 
        
        output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)

        num_labels = output[0]
        labels = output[1]
        stats = output[2]

        self.centroids = output[3]

        for c in self.centroids :

            self.mean_centroids[0] += c[0]/len(self.centroids)
            self.mean_centroids[1] += c[1]/len(self.centroids)

        self.img_final = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        #for c in self.centroids :
            #self.img_final[int(c[1]) -20: int(c[1])+20, int(c[0])-20 : int(c[0])+20] = [0,255,0]
        """
    """
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
    """
def show(org_image1, detection_image1, org_image2, detection_image2):
    plt.subplot(2, 2, 1), plt.imshow(org_image1, cmap="gray"), plt.title('org1')
    plt.xticks([]), plt.yticks([])
    plt.subplot(2, 2, 2), plt.imshow(detection_image1, cmap="gray"), plt.title('detection 1')
    plt.xticks([]), plt.yticks([])
    plt.subplot(2, 2, 3), plt.imshow(org_image2, cmap="gray"), plt.title('org2')
    plt.xticks([]), plt.yticks([])
    plt.subplot(2, 2, 4), plt.imshow(detection_image2, cmap="gray"), plt.title('detection 2')
    plt.xticks([]), plt.yticks([])
    plt.savefig('./testing_detected/output/result_test_8_9.png')
    plt.show()



