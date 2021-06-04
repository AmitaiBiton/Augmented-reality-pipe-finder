import math
import cv2
import numpy as np
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import argparse
import pyrealsense2 as rs
from depth_filters import filter_frames
from tracking_by_image_processing import LineTracking


class pipe:
    def __init__(self , x ,y ,depth):
        self.pixelX = x
        self.pixelY = y
        self.pixelDepth = depth

"""calculate the distance between two points (objects) """
def calculate_distance(self,x,y):
        color_intrin = self.color_intrin
        ix,iy = self.ix, self.iy
        udist = self.depth_frame.get_distance(ix,iy)
        vdist = self.depth_frame.get_distance(x, y)
        #print udist,vdist
        """from pixel to point to calculate the distance """
        point1 = rs.rs2_deproject_pixel_to_point(color_intrin, [ix, iy], udist)
        point2 = rs.rs2_deproject_pixel_to_point(color_intrin, [x, y], vdist)
        #print str(point1)+str(point2)
        """by distance between p1 to realsense camera  and p2 distance from camera  calculate the remainder """
        dist = math.sqrt(
            math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2) + math.pow(
                point1[2] - point2[2], 2))
        print ('distance: '+ str(dist))
        return dist

def read_aligned_frames():
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_device_from_file("./test/obj1.bag")
    pipe.start(cfg)
    align_to = rs.stream.color
    align = rs.align(align_to)
        # Skip 5 first frames to give the Auto-Exposure time to adjust
    for x in range(5):
        pipe.wait_for_frames()

        # Create colorizer object

        # Streaming loop

        # Store next frameset for later processing:
    frameset = pipe.wait_for_frames()
    aligned_frames = align.process(frameset)
    aligned_depth_frame = aligned_frames.get_depth_frame()

    return aligned_depth_frame



def read_color_image():
    image  = cv2.imread("./output/newimage.jpg",0)
    print(image.shape)
    canny = cv2.Canny(image , 0 , 100)
    canny=cv2.dilate(canny,np.ones((5,5)))
    pipe_detected_canny   = []
    for i in range(1080):
        for j in  range(1920):
            if canny[i][j]>0:
                pipe_detected_canny.append((i,j))

    return pipe_detected_canny ,canny


"""get the image we detect on the pipe and get from the image the points of the pipe return list of  (X,Y)"""
def get_points_from_detection_pipe(tracking):
    pipe_detected_list = []
    for i in range(1080):
        for j in range(1920):
            if tracking.img_final[i][j] > 0:
                pipe_detected_list.append((i, j))
    return  pipe_detected_list
"""show function show the result of the org image  , detected image  , and depth+object detection """
def show(image  ,canny , result):
    plt.subplot(131), plt.imshow(image, cmap="gray"), plt.title('color_image')
    plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(canny, cmap="gray"), plt.title('canny')
    plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(result, cmap="gray"), plt.title('Result = canny && depth ')
    plt.xticks([]), plt.yticks([])
    plt.show()


#def distance_between_objects(aligned_depth_frame):
"""
doing AND opertor between depth data and object detection image 
 the result will be only pipe that have depth none zero and detection =true 
 """
def calculate_pipe_depth_for_any_points(aligned_depth_frame, pipe_detected_canny):
    pipe_detected_depth = []
    for l in pipe_detected_canny:
        print(l)
        if l[1] < aligned_depth_frame.get_width() and l[0] < aligned_depth_frame.get_height():
            d = aligned_depth_frame.get_distance(l[1] ,l[0])
            pipe_detected_depth.append((l ,d))
    return pipe_detected_depth

"""calculate the distance between two points (objects) """

def calculate_distance( color_intrin, depth_frame , x1 ,y1, x2, y2):
    udist = depth_frame[x1, y1]
    vdist = depth_frame[x2, y2]
    print (udist,vdist)
    print(udist , vdist)
    point1 = rs.rs2_deproject_pixel_to_point(color_intrin, [x1, y1], udist)
    point2 = rs.rs2_deproject_pixel_to_point(color_intrin, [x2, y2], vdist)
    print (str(point1)+str(point2))

    dist = np.math.sqrt(
        np.math.pow(point1[0] - point2[0], 2) + np.math.pow(point1[1] - point2[1], 2) + np.math.pow(
            point1[2] - point2[2], 2))
    # print 'distance: '+ str(dist)
    return dist



if __name__ == '__main__':

    color  = cv2.imread("./output/newimage.jpg",1)

    # create new stream from bag file to get the same rusolotion
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_device_from_file("./test/obj1.bag")
    pipe.start(cfg)
    align_to = rs.stream.color
    align = rs.align(align_to)

    # Skip 5 first frames to give the Auto-Exposure time to adjust
    for x in range(10):
        pipe.wait_for_frames()
    """to compera the rusolotions between depth data and color data
    depth org = 848/480 , color image = 1080/1920 change to both 1080/1920"""
    frameset = pipe.wait_for_frames()
    aligned_frames = align.process(frameset)
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame  = aligned_frames.get_color_frame()
    color_image = np.asanyarray(aligned_depth_frame.get_data())
    color_intrin = color_frame.profile.as_video_stream_profile().intrinsics

    colorized_depth, depth_frame = filter_frames() # data 848X480 , color depth image 848X480
    depth_frame = depth_frame.as_depth_frame()

    #aligned_depth = read_aligned_frames()# pic 1920X1080 depth data
    """
    pipe_detected_canny ,canny = read_color_image() # color image 1920X1080 , canny
    pipe_detected_depth = calculate_pipe_depth_for_any_points(aligned_depth_frame,pipe_detected_canny)
    
    depth_frame = np.asanyarray(depth_frame.get_data())

    print("asasasasasasasa" , calculate_distance(color_intrin, depth_frame, 44,437,34,720))
    depth_and_canny = np.zeros((1080 ,1920))
    for d in pipe_detected_depth:
        if d[1]>0:
            depth_and_canny[d[0]] = d[1]
    colorizer = rs.colorizer();
    depth_color_frame = colorizer.colorize(aligned_depth_frame)
    colorized_depth = np.asanyarray(depth_color_frame.get_data())
    #show(color  , canny  , depth_and_canny )
    """
    pipe.stop()
    # do the object detection by image processing
    tracking  = LineTracking('./output/newimage.jpg')
    tracking.processing()
    tracking.img_final = tracking.img_final[:,:,0]

    """
        get the points where  detection by image processing is 255
    """
    pipe_detected_list  = get_points_from_detection_pipe(tracking)

    # after we get the pixel that we catch in object detection by image processing sand a list of the points
    # and get the depth value for thay
    pipe_detected_depth = calculate_pipe_depth_for_any_points(aligned_depth_frame,pipe_detected_list)

    #print("asasasasasasasa" , calculate_distance(color_intrin, depth_frame, 44,437,34,720))

    # doing AND operator between the depth data and object detection
    depth_and_canny = np.zeros((1080 ,1920))
    for d in pipe_detected_depth:
        if d[1]>0:
            depth_and_canny[d[0]] = d[1]
    colorizer = rs.colorizer();
    depth_color_frame = colorizer.colorize(aligned_depth_frame)
    colorized_depth = np.asanyarray(depth_color_frame.get_data())
    # showing results
    show(color  , tracking.img_final , depth_and_canny )



