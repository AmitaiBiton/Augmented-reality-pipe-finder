from pyrealsense2.pyrealsense2 import depth_frame
import pyrealsense2 as rs
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
from numpy.linalg import inv
from detect_Qr_code import detect_qr_code
from pipe_detected_by_image_processing import read_aligned_frames
from streaming_from_bag_file import streaming_from_bag_file
import cv2
import  numpy as np

from tracking_by_image_processing import LineTracking

def add_vector_one(list):
    new_list=[]
    for i in range(list.shape[0]):
        t1 = []
        for j in range(list.shape[1] + 1):
            if j == 3:
                t1.append(1)
            else:
                t1.append(int(list[i][j]))
        new_list.append(t1)
    return new_list

def build_reference_points(point1,point2):
    point_list1 = []
    point_list2 = []
    point_list1.append((point1[0][0], point1[0][1]))
    point_list1.append((point1[0][0] + 1, point1[0][1] + 1))
    point_list1.append((point1[0][0] - 1, point1[0][1] - 1))
    point_list1.append((point1[0][0] + 2, point1[0][1] + 2))
    point_list2.append((point2[0][0], point2[0][1]))
    point_list2.append((point2[0][0] + 1, point2[0][1] + 1))
    point_list2.append((point2[0][0] - 1, point2[0][1] - 1))
    point_list2.append((point2[0][0] + 2, point2[0][1] + 2))
    return  point_list1,point_list2

def pixel_uv_to_points_xyz(list):
    points=[]
    for i in range(len(list)):
        udist1 = depth_data_array[list[i][0], list[i][1]]
        points.append(rs.rs2_deproject_pixel_to_point(color_intrin, [list[i][0], list[i][1]], udist1))
    return points


def get_pixel_pipes():
    list_pixel_pipes=[]
    tracking = LineTracking('./output/new5.jpg')
    tracking.processing()
    tracking.img_final = tracking.img_final[:, :, 0]
    for i in range(tracking.img_final.shape[0]):
        for j in range(tracking.img_final.shape[1]):
            if tracking.img_final[i][j] > 0:
                list_pixel_pipes.append((i, j))
    return list_pixel_pipes




streaming_from_bag_file('./scaning/obj5.bag' ,'./output/new6.jpg' )
image1 = cv2.imread('./output/new6.jpg')
streaming_from_bag_file('./scaning_2/obj5.bag' ,'./output_2/new6.jpg' )
image2 = cv2.imread('./output_2/new6.jpg')
image_QR_detector1 , point1 = detect_qr_code(image1)
image_QR_detector2 , point2 = detect_qr_code(image2)

point_list1 ,point_list2 = build_reference_points(point1,point2)

aligned_depth_frame, aligned_frames = read_aligned_frames('./scaning/obj5.bag')
color_frame = aligned_frames.get_color_frame()

depth_data_array = np.asanyarray(aligned_depth_frame.get_data())
color_intrin = color_frame.profile.as_video_stream_profile().intrinsics

points1 = pixel_uv_to_points_xyz(point_list1)
points2 = pixel_uv_to_points_xyz(point_list2)

points1 = np.array(points1)
points2 = np.array(points2)


p1 = add_vector_one(points1)
p2 = add_vector_one((points2))
matrix_A  = np.array(p1)
matrix_B = np.array(p2)
print(matrix_A)
print(matrix_B)
matrix_A_invers = inv(matrix_A)
matrix_RT = np.dot(matrix_A_invers , matrix_B)
print(matrix_RT)

list_pixel_pipes = get_pixel_pipes()
list_point_pipes = []

list_point_pipes = pixel_uv_to_points_xyz(list_pixel_pipes)
list_point_pipes = np.array(list_point_pipes)
points_pipes_3D = add_vector_one(list_point_pipes)

#print(points_pipes_3D[0] , list_point_pipes[0])