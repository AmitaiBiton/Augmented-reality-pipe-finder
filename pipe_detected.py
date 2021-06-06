import cv2
import numpy as np
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import argparse
import pyrealsense2 as rs
from depth_filters import filter_frames
class pipe:
    def __init__(self , x ,y ,depth):
        self.pixelX = x
        self.pixelY = y
        self.pixelDepth = depth


def calculate_distance(self,x,y):
        color_intrin = self.color_intrin
        ix,iy = self.ix, self.iy
        udist = self.depth_frame.get_distance(ix,iy)
        vdist = self.depth_frame.get_distance(x, y)
        #print udist,vdist

        point1 = rs.rs2_deproject_pixel_to_point(color_intrin, [ix, iy], udist)
        point2 = rs.rs2_deproject_pixel_to_point(color_intrin, [x, y], vdist)
        #print str(point1)+str(point2)

        dist = np.math.sqrt(
            np.math.pow(point1[0] - point2[0], 2) + np.math.pow(point1[1] - point2[1], 2) + np.math.pow(
                point1[2] - point2[2], 2))
        print ('distance: '+ str(dist))
        return dist



#depth_image ,depth_frame = filter_frames()


#____ 1 : get the pipe from color image
#_____2 : get the depth data from frame image
#_____ 3 : get per pixel color and depth data
#______4 : show the results
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

def show(image  ,canny , result):
    plt.subplot(131), plt.imshow(image, cmap="gray"), plt.title('color_image')
    plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(canny, cmap="gray"), plt.title('canny')
    plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(result, cmap="gray"), plt.title('Result = canny && depth ')
    plt.xticks([]), plt.yticks([])
    plt.show()


#def distance_between_objects(aligned_depth_frame):

def calculate_pipe_depth_for_any_points(aligned_depth_frame, pipe_detected_canny):
    pipe_detected_depth = []
    for l in pipe_detected_canny:
        if l[1] < aligned_depth_frame.get_width() and l[0] < aligned_depth_frame.get_height():
            d = aligned_depth_frame.get_distance(l[1] ,l[0])
            pipe_detected_depth.append((l ,d))
    return pipe_detected_depth

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

    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_device_from_file("./test/obj1.bag")
    pipe.start(cfg)
    align_to = rs.stream.color
    align = rs.align(align_to)

    # Skip 5 first frames to give the Auto-Exposure time to adjust
    for x in range(10):
        pipe.wait_for_frames()
    frameset = pipe.wait_for_frames()
    aligned_frames = align.process(frameset)
    aligned_depth_frame = aligned_frames.get_depth_frame()

    color_frame  = aligned_frames.get_color_frame()
    color_image = np.asanyarray(aligned_depth_frame.get_data())
    color_intrin = color_frame.profile.as_video_stream_profile().intrinsics

    colorized_depth, depth_frame = filter_frames() # data 848X480 , color depth image 848X480
    depth_frame = depth_frame.as_depth_frame()

    #aligned_depth = read_aligned_frames()# pic 1920X1080 depth data

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
    show(color  , canny  , depth_and_canny )
    pipe.stop()
