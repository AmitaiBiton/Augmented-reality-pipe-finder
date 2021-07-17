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
import torch
"""
step 1: build reference points
build points that we detected on qr code  
need to build 4 points for any scan : first and second 

step 2: pixel u,v to points x,y,z (de_projection)
take the point U,V and calculate the points on 3D X,Y,Z

step3: add vector one
matrix from 4X3 to 4X4

step 4:
calculate RT matrix by using A^-1B = RT

step 5: 
find all the pixel that represent the pipe on 2D image

step 6:
all the points of the pipe de projection to 3D points

step 7: 
pints 3D of pipe dot RT matrix 

step 8: 
projection the results on scan two 
"""

from tracking_by_image_processing import LineTracking

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

def pixel_uv_to_points_xyz(list):
    points=[]
    for i in range(len(list)):
        udist1 = depth_data_array[list[i][0], list[i][1]]
        #udist1  = depth_frame.get_distance(list[i][0], list[i][1])
        points.append(rs.rs2_deproject_pixel_to_point(depth_intrin, [list[i][0], list[i][1]], udist1))
    return points

def get_pixel_pipes(image):
    list_pixel_pipes=[]

    tracking = LineTracking(image)
    tracking.processing()
    tracking.img_final = tracking.img_final[:, :, 0]
    for i in range(tracking.img_final.shape[0]):
        for j in range(tracking.img_final.shape[1]):
            if tracking.img_final[i][j] > 0:
                list_pixel_pipes.append((image1[i][j]))
    return list_pixel_pipes

def image_from_2D_to_3D(image):
    list_image = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            udist1 = depth_data_array[i,j]
            # udist1  = depth_frame.get_distance(list[i][0], list[i][1])
            list_image.append(rs.rs2_deproject_pixel_to_point(color_intrin, [j,i], udist1))
    return  list_image

device = "cpu"
if (torch.cuda.is_available()):
    device = "cuda"
print(device)
image1 = streaming_from_bag_file('./pipe_finder/salon/1.bag')
image2 = streaming_from_bag_file('./pipe_finder/salon/2.bag')


img2 = np.copy(image2)
#image_QR_detector1 , point1 = detect_qr_code(image1)
#image_QR_detector2 , point2 = detect_qr_code(image2)

#point_list1 ,point_list2 = build_reference_points(point1,point2)
point_list1 = [[248,676],[367,675],[367,798],[248,795]]
point_list2 = [[246,674],[365,676],[365,798],[246,795]]
aligned_depth_frame, aligned_frames = read_aligned_frames('./scaning/obj5.bag')
color_frame = aligned_frames.get_color_frame()
depth_frame = aligned_frames.get_depth_frame()
depth_data_array = np.asanyarray(aligned_depth_frame.get_data())
color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics

depth_to_color_extrin = depth_frame.profile.get_extrinsics_to(color_frame.profile)


points1 = pixel_uv_to_points_xyz(point_list1)
points2 = pixel_uv_to_points_xyz(point_list2)

points1 = np.array(points1)
points2 = np.array(points2)


p1 = add_vector_one(points1)
p2 = add_vector_one((points2))
#p1=np.hstack((points1,np.ones((points1.shape[0],1))))
A = np.array(p1)
B = np.array(p2)
#

#matrix_RT = np.dot(matrix_A_invers,B)
matrix_RT = np.float64(np.dot(B.T,inv(A.T)))

points_image_A = image_from_2D_to_3D(image1)
#points_image_B = image_from_2D_to_3D(image2)

points_image_A = np.array(points_image_A)
points_image_A = add_vector_one(points_image_A)

points_image_A = np.array(points_image_A)
image1_position_image2 = np.dot(matrix_RT,points_image_A.T)

final_pixel_projection = []
for row in image1_position_image2.T:
    point = row[:3]
    #color_point = rs.rs2_transform_point_to_point(depth_to_color_extrin, depth_point)
    color_pixel = rs.rs2_project_point_to_pixel(color_intrin, point)
    if  math.isnan(color_pixel[0])!= True and math.isnan(color_pixel[1])!= True:
        final_pixel_projection.append((int(color_pixel[0]), int(color_pixel[1])))

final_pixel_projection = np.array(final_pixel_projection)
list_value_color = []
for i in range(image1.shape[0]):
    for j in range(image1.shape[1]):
        list_value_color.append((image1[i][j]))


final_pixel_projection = np.array(final_pixel_projection)

list_value_color = np.reshape(list_value_color, (1080, 1920,3))
final_pixel_projection = np.reshape(final_pixel_projection, (1080, 1920,2))

new_color_image_localizatiion = np.copy(image2)
new_color_image_localizatiion[:, :, :] = 155

for i in range(final_pixel_projection.shape[0]):
    for j in range(final_pixel_projection.shape[1]):
        if final_pixel_projection[i][j][0] < 0:
            final_pixel_projection[i][j][0] = 0
        if final_pixel_projection[i][j][1] < 0:
            final_pixel_projection[i][j][1] = 0
        if final_pixel_projection[i][j][0] >= 1800:
            final_pixel_projection[i][j][0] = 0
        if final_pixel_projection[i][j][1] >= 1080:
            final_pixel_projection[i][j][1] = 0
image  = cv2.imread('./pipe_finder/salon/1.jpg')
list_pixel_pipes = get_pixel_pipes(image)
print(list_pixel_pipes)
color_exist = False
for i in range(list_value_color.shape[0]):
    for j in range(list_value_color.shape[1]):
       image2[i][j]= list_value_color[final_pixel_projection[i][j][1]][final_pixel_projection[i][j][0]]

cv2.imshow("new imaghe" , image2)
cv2.waitKey()

