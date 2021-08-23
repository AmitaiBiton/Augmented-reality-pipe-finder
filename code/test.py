






from pyrealsense2.pyrealsense2 import depth_frame
import pyrealsense2 as rs
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
from numpy.linalg import inv
from detect_Qr_code import detect_qr_code
from pipe_detected_by_image_processing import read_aligned_frames
from streaming_from_bag_file import streaming_from_bag_file
import cv2
import math
import  numpy as np



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
    return np.array(new_list)

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
        udist1 = depth_data_array[list[i][0], list[i][0]]
        points.append(rs.rs2_deproject_pixel_to_point(color_intrin, [list[i][0], list[i][1]], udist1))
    return points

def image_from_2D_to_3D(image):
    list_image = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            udist1 = depth_data_array[i,j]
            list_image.append(rs.rs2_deproject_pixel_to_point(color_intrin, [i,j], udist1))
    return  np.array(list_image)



streaming_from_bag_file('./scaning/obj5.bag' ,'./output/new6.jpg' )
image1 = cv2.imread('./output/new6.jpg')
streaming_from_bag_file('./scaning_2/obj5.bag' ,'./output_2/new6.jpg' )
image2 = cv2.imread('./output_2/new6.jpg')

img2 = np.copy(image2)
image_QR_detector1 , point1 = detect_qr_code(image1)
image_QR_detector2 , point2 = detect_qr_code(image2)
pixels_A_QR ,pixels_B_QR = build_reference_points(point1,point2)

aligned_depth_frame, aligned_frames = read_aligned_frames('./scaning/obj5.bag')
color_frame = aligned_frames.get_color_frame()
depth_frame = aligned_frames.get_depth_frame()
depth_data_array = np.asanyarray(aligned_depth_frame.get_data())
color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
depth_to_color_extrin = depth_frame.profile.get_extrinsics_to(color_frame.profile)


points_QR_A = pixel_uv_to_points_xyz(pixels_A_QR)
points_QR_B = pixel_uv_to_points_xyz(pixels_B_QR)
points_QR_A= np.array(points_QR_A)
points_QR_B= np.array(points_QR_B)

points_QR_A = add_vector_one(points_QR_A)
points_QR_B = add_vector_one(points_QR_B)

invers_A = inv(points_QR_A.T)
matrix_RT=np.dot(points_QR_B.T,invers_A)

#all image from 2D to 3D
points_image_A = image_from_2D_to_3D(image1)

points_image_A = add_vector_one(points_image_A)

image1_position_image2 = np.dot(matrix_RT,points_image_A.T)

image1_position_image2 = image1_position_image2[:3]
image1_position_image2 = image1_position_image2.T
image1_position_image2 = np.reshape(image1_position_image2, (1080, 1920,3))

final_pixel_projection = np.zeros((1080,1920,2))
for i in range(1080):
    for j in range(1920):
        depth_point = depth_data_array[i,j]
        final_pixel_projection[i][j] = rs.rs2_project_point_to_pixel(color_intrin,image1_position_image2[i][j])
print(final_pixel_projection)
new_color_image_localizatiion = np.copy(image2)
new_color_image_localizatiion[:, :, :] = 155

for i in range(image2.shape[0]):
    for j in range(image2.shape[1]):
        image2[i][j] = image2[image1_position_image2[i][j][0]][image1_position_image2[i][j][1]]
print(image2)
cv2.imshow("fthrt",image2)
cv2.waitKey()