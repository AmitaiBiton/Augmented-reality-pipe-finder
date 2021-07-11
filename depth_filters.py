import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs
import cv2

def filter_frames():
    pipe = rs.pipeline()
    cfg = rs.config()

    cfg.enable_device_from_file("./scaning/obj5.bag")
    pipe.start(cfg)

    align_to = rs.stream.color
    align = rs.align(align_to)
    # Skip 5 first frames to give the Auto-Exposure time to adjust
    for x in range(5):
        pipe.wait_for_frames()

    frameset = pipe.wait_for_frames()
    aligned_frames = align.process(frameset)
    depth_frame = aligned_frames.get_depth_frame()

    # Cleanup:
    pipe.stop()
    print("Frames Captured")

    colorizer = rs.colorizer()
    """create the colorizer for depth data to color data map """
    colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())

    """see the data without filter as color image """
    plt.rcParams["axes.grid"] = False
    plt.rcParams['figure.figsize'] = [8, 4]
    plt.imshow(colorized_depth)
    #plt.show()
    """
    when is the resolutions is bad the filter will doing filter on this area  after that is also do hole filing 
    using none zero pixel 
    """
    decimation = rs.decimation_filter()
    decimated_depth = decimation.process(depth_frame)
    colorized_depth = np.asanyarray(colorizer.colorize(decimated_depth).get_data())
    plt.imshow(colorized_depth)
    #plt.show()

    decimation.set_option(rs.option.filter_magnitude, 4)
    decimated_depth = decimation.process(depth_frame)
    colorized_depth = np.asanyarray(colorizer.colorize(decimated_depth).get_data())
    plt.imshow(colorized_depth)
    #plt.show()
    """if some area is reconstructed so is   enhance this area  by transfrom"""
    spatial = rs.spatial_filter()
    filtered_depth = spatial.process(depth_frame)
    colorized_depth = np.asanyarray(colorizer.colorize(filtered_depth).get_data())
    plt.imshow(colorized_depth)
    #plt.show()
    """set the parameters """
    spatial.set_option(rs.option.filter_magnitude, 2)
    spatial.set_option(rs.option.filter_smooth_alpha, 0.5)
    spatial.set_option(rs.option.filter_smooth_delta, 18)
    filtered_depth = spatial.process(depth_frame)
    colorized_depth = np.asanyarray(colorizer.colorize(filtered_depth).get_data())
    plt.imshow(colorized_depth)
    #plt.show()

    spatial.set_option(rs.option.holes_fill, 2)
    filtered_depth = spatial.process(depth_frame)
    colorized_depth = np.asanyarray(colorizer.colorize(filtered_depth).get_data())
    plt.imshow(colorized_depth)
    #plt.show()

    profile = pipe.start(cfg)
    """list of the frames in this stream """
    frames = []
    for x in range(15):
        frameset = pipe.wait_for_frames()
        aligned_frames = align.process(frameset)
        frames.append(aligned_frames .get_depth_frame())

    pipe.stop()
    print("Frames Captured")
    temporal = rs.temporal_filter()
    for x in range(10):
        temp_filtered = temporal.process(frames[x])
    colorized_depth = np.asanyarray(colorizer.colorize(temp_filtered).get_data())
    plt.imshow(colorized_depth)
    hole_filling = rs.hole_filling_filter()
    filled_depth = hole_filling.process(depth_frame)
    colorized_depth = np.asanyarray(colorizer.colorize(filled_depth).get_data())
    plt.imshow(colorized_depth)
    #plt.show()
    #
    depth_to_disparity = rs.disparity_transform(True)
    disparity_to_depth = rs.disparity_transform(False)
    """for every frame do the filter and get the bast frame without zero area  """
    for x in range(15):
        frame = frames[x]
        #frame = decimation.process(frame)
        frame = depth_to_disparity.process(frame)
        frame = spatial.process(frame)
        frame = temporal.process(frame)
        frame = disparity_to_depth.process(frame)
        frame = hole_filling.process(frame)
    colorized_depth = np.asanyarray(colorizer.colorize(frame).get_data())
    plt.imshow(colorized_depth)
    plt.show()
    depth_frame = depth_frame.as_depth_frame()
    d = np.asanyarray(frame.get_data())
    print(d.shape)

    counter=0
    for i in range(depth_frame.get_width()):
        for j in  range(depth_frame.get_height()):
            if d[j][i]==0:
                counter+=1
    print("counter zero =  " , counter)


    return colorized_depth ,frame

filter_frames()