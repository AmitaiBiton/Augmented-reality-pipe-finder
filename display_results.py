import logging
import pyrealsense2 as rs

import cv2
import mouse
import numpy as np
from pynput.mouse import Button, Controller
from pynput.mouse import Listener

# read image
from pipe_detected_by_image_processing import read_aligned_frames, calculate_distance

def mouse_click(event, x, y, flags, args):
    color_intrin = args[0]
    img = args[1]
    depth_data_array = args[2]
    global refPt
    refPt = args[3]
    # to check if left mouse
    # button was clicked

    if event == cv2.EVENT_LBUTTONDOWN:
        # font for left click event
        font = cv2.FONT_HERSHEY_TRIPLEX
        point1 = mouse.get_position()
        LB = "p1"

    # display that left button
        # was clicked.
        x = point1[0]
        y= point1[1]
        refPt.append((x, y))
        if len(refPt)==2:
            LB = "p2"
        cv2.putText(img, LB, (x, y),
                    font, 1,
                    (255, 255, 0),
                    2)
        if len(refPt) % 2==0:
            distance  = calculate_distance(color_intrin, depth_data_array, refPt[len(refPt)-2][1],refPt[len(refPt)-2][0],refPt[len(refPt)-1][1], refPt[len(refPt)-1][0])
            LB = "distance = {}cm".format(distance/10)
            cv2.line(img, (refPt[len(refPt)-2][0]+45,refPt[len(refPt)-2][1]), (refPt[len(refPt)-1][0], refPt[len(refPt)-1][1]),  (0, 255, 0), 9)
            cv2.putText(img, LB, (100,int(refPt[len(refPt)-2][1] + (refPt[len(refPt)-1][1]-refPt[len(refPt)-2][1] )/2 )),
                        font, 1,
                        (0, 0, 0),
                        2)
            refPt = []
        cv2.imshow('image',img)

def display(image , path_file):
    #img = cv2.imread(path_image)
    aligned_depth_frame, aligned_frames = read_aligned_frames(path_file)
    color_frame = aligned_frames.get_color_frame()
    depth_data_array = np.asanyarray(aligned_depth_frame.get_data())
    color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
    # show image
    refPt = []
    cv2.imshow('image', image)
    # define the events for the
    # mouse_click.
    cv2.setMouseCallback('image',  mouse_click ,(color_intrin , image , depth_data_array ,refPt))

    cv2.waitKey(0)

