import cv2
import numpy as np
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import argparse
import pyrealsense2 as rs
import pyrealsense2 as rs
import numpy as np
import pyrealsense2 as rs
from pynput.mouse import Listener



        # to check if right mouse
import mouse
def show_distance(event, x, y, args, params):
    global point
    point = (x, y)

if __name__ == '__main__':

    point = (400, 300)
    # Create mouse event
    cv2.namedWindow("Color frame")
    cv2.setMouseCallback("Color frame", show_distance)
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_device_from_file("./test/obj1.bag")
    pipe.start(cfg)
    align_to = rs.stream.color
    align = rs.align(align_to)

    cv2.namedWindow("Color frame")
    cv2.setMouseCallback("Color frame", show_distance)



    # Create opencv window to render image in
    while True:
        frameset = pipe.wait_for_frames()
        aligned_frames = align.process(frameset)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        color_intrin = color_frame.profile.as_video_stream_profile().intrinsics

        color_frame = np.asanyarray(color_frame.get_data())
        depth_frame = np.asanyarray(depth_frame.get_data())
        udist = depth_frame[point[1],point[0]]
        print("before:" , point)
        point1 = rs.rs2_deproject_pixel_to_point(color_intrin, [point[0] ,point[1]], udist)
        color_pixel = rs.rs2_project_point_to_pixel(color_intrin, point1)
        print("after:", color_pixel)
        # Show distance for a specific point
        point2 =rs.rs2_deproject_pixel_to_point(color_intrin, [point[0] ,point[1]], udist)
        cv2.circle(color_frame, point, 4, (0, 0, 255))
        #distance = depth_frame[point[1], point[0]]
        distance  = point1
        #print(point , distance)
        cv2.putText(color_frame, "{}X,Y,Z:".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 0, 0), 2)
        cv2.putText(color_frame, "{}U,V".format(point), (point[0], point[1] - 50), cv2.FONT_HERSHEY_PLAIN, 4,
                    (0, 0, 0), 2)
        cv2.imshow("depth frame", depth_frame)
        cv2.imshow("Color frame", color_frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

