import pyrealsense2 as rs
import numpy as np
import cv2
import pyautogui as pag

class Scan:
    def __init__(self , width_depth , height_depth  ,width_color , height_color , bag_file):
        self.width_color =width_color
        self.height_color = height_color
        self.height_depth = height_depth
        self.width_depth=width_depth
        self.bag_file = bag_file


def realsense_streaming(path):
    """
    if number_scan == 1:
        final_path ='scaning'+path+'.bag'
    if number_scan ==2:
        final_path = 'scaning_2' + path + '.bag'
     #    s  = Scan(848,480,1920,1080,final_path)
    """
    s  = Scan(848,480,1920,1080,path)

    #Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, s.width_color, s.height_color, rs.format.rgb8, 30)
    config.enable_stream(rs.stream.depth, s.width_depth, s.height_depth, rs.format.z16, 30)

    config.enable_record_to_file(s.bag_file)
    rs_context = rs.context()

    while len(rs_context.query_all_sensors()) == 0:
        pag.alert(text="please connect camera to you are computer with USB3" , title=" Disconnect camera ")
    profile  = pipeline.start(config)
    """
    sensor_dep = profile.get_device().first_depth_sensor()
    exp = sensor_dep.get_option(rs.option.exposure)

    """
    e1 = cv2.getTickCount()

    try:
        while True:

            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

# Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Apply colormap on depth image (image must be converted to8-bit per pixel first)
            depth_colormap =cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.01),cv2.COLORMAP_JET)

            # Stack both images horizontally
            #images = np.hstack((color_image, depth_colormap))

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', color_image)
            cv2.waitKey(1)
            e2 = cv2.getTickCount()
            t = (e2 - e1) / cv2.getTickFrequency()
            if t>10: # change it to record what length of video you are interested in
                print("Done!")
                break

    finally:
    # Stop streaming
        pipeline.stop()
realsense_streaming('./scaning/a.bag')