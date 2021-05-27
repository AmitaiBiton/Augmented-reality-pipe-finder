
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
def read_depth_from_stream():
    depth_list = ""
    list=[]
    try:
        # Create pipeline
        pipeline = rs.pipeline()

        # Create a config object
        config = rs.config()

        # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
        rs.config.enable_device_from_file(config, args.input)

        # Configure the pipeline to stream the depth stream
        # Change this parameters according to the recorded bag file resolution
        config.enable_stream(rs.stream.depth, rs.format.z16, 30)

        # Start streaming from file
        pipeline.start(config)

        # Create opencv window to render image in
        cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)

        # Create colorizer object
        colorizer = rs.colorizer();
        list_Depth_images = []
        # Streaming loop
        x =0
        y =0
        count=0
        depth_list = ""
        while True:
            # Get frameset of depth
            for i in range(6):
                frames = pipeline.wait_for_frames()
            count += 1
            # Get depth frame
            depth_frame = frames.get_depth_frame()
            zDepth = depth_frame.get_distance(100,100)
            if not depth_frame: continue
            width = depth_frame.get_width()
            height = depth_frame.get_height()
            # print(width,height)

            # Calculate distance
            dist_to_center = depth_frame.get_distance(int(width / 2), int(height / 2))
            print('The camera is facing an object:', dist_to_center, 'meters away')
            # Colorize depth frame to jet colormap
            depth_color_frame = colorizer.colorize(depth_frame)

            # Convert depth_frame to numpy array to render image in opencv
            depth_color_image = np.asanyarray(depth_color_frame.get_data())

            #list_Depth_images.append(depth_color_image)
            list  = []
            # Render image in opencv window
            cv2.imshow("Depth Stream", depth_color_image)
            key = cv2.waitKey(1)
            # if pressed escape exit program
            if key == 27:
                cv2.destroyAllWindows()
                break
            if count == 3:
                coverage = [0] * 64
                for y in range(depth_frame.get_height()):
                    for x in range(depth_frame.get_width()):
                        dist = depth_frame.get_distance(x, y)
                        print(dist)


                break
            #cv2.imwrite('./color_images/New Bitmap .bmp', list_Depth_images[15])
    finally:
        pass
read_depth_from_stream()
