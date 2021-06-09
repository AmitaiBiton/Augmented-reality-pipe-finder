import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import pyrealsense2 as rs
from depth_filters import filter_frames
from pipe_detected_by_image_processing import read_aligned_frames
from tracking_by_image_processing import LineTracking


def calculate_distance( color_intrin, depth_frame , x1 ,y1, x2, y2):
    udist = depth_frame[x1, y1]
    vdist = depth_frame[x2, y2]

    point1 = rs.rs2_deproject_pixel_to_point(color_intrin, [x1, y1], udist)
    point2 = rs.rs2_deproject_pixel_to_point(color_intrin, [x2, y2], vdist)

    dist = np.math.sqrt(
        np.math.pow(point1[0] - point2[0], 2) + np.math.pow(point1[1] - point2[1], 2) + np.math.pow(
            point1[2] - point2[2], 2))
    # print 'distance: '+ str(dist)
    return dist

aligned_depth_frame , aligned_frames = read_aligned_frames()
color_frame  = aligned_frames.get_color_frame()
depth_data_array = np.asanyarray(aligned_depth_frame.get_data())
color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
print("asasasasasasasa" , calculate_distance(color_intrin, depth_data_array, 0,50,1079,50))
