

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

# Create object for parsing command-line options
parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
                                Remember to change the stream fps and format to match the recorded.")
# Add argument which takes path to a bag file as an input
parser.add_argument("-i", "--input", type=str, help="Path to the bag file")
# Parse the command line arguments to an object
args = parser.parse_args()
# Safety if no parameter have been given
if not args.input:
    print("No input paramater have been given.")
    print("For help type --help")
    exit()
# Check if the given file have bag extension
if os.path.splitext(args.input)[1] != ".bag":
    print("The given file is not of correct file format.")
    print("Only .bag files are accepted")
    exit()

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, args.input)

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
        if count == 150:
            break




    cv2.imwrite('./output/newimage.jpg', list_color_images[10])
    cv2.imshow("color image " , list_color_images[1])
    cv2.waitKeyEx()
finally:
    pass