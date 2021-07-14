
# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path
def streaming_from_bag_file(path_file ):
    try:
        # Create pipeline
        pipeline = rs.pipeline()

        # Create a config object
        config = rs.config()

        # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
        rs.config.enable_device_from_file(config,path_file )

        # Configure the pipeline to stream the depth stream
        # Change this parameters according to the recorded bag file resolution
        config.enable_stream(rs.stream.color)

        # Start streaming from file
        pipeline.start(config)

        # Create opencv window to render image in
        cv2.namedWindow("Color Stream", cv2.WINDOW_AUTOSIZE)
        list_color_images = []

        # Create colorizer object
        colorizer = rs.colorizer();
        count=0
        # Streaming loop
        while True:
            # Get frameset of depth
            frames = pipeline.wait_for_frames()
            count +=1
            # Get Color frame
            frame_color = frames.get_color_frame()

            # Colorize Color frame to jet colormap
            color_frame = colorizer.colorize(frame_color)

            # Convert depth_frame to numpy array to render image in opencv
            color_image = np.asanyarray(color_frame.get_data())
            list_color_images.append(color_image)

            # Render image in opencv window
            cv2.imshow("Color Stream", color_image)
            key = cv2.waitKey(1)
            # if pressed escape exit program
            if key == 27:
                cv2.destroyAllWindows()
                break
            if count == 15:
                break
        cv2.imshow("color image " , list_color_images[1])
        cv2.waitKeyEx()
        return list_color_images[10]
    finally:
        pass