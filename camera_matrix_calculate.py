from detect_Qr_code import detect_qr_code
from streaming_from_bag_file import streaming_from_bag_file
import cv2
streaming_from_bag_file('./scaning/obj5.bag' ,'./output/new6.jpg' )
image1 = cv2.imread('./output/new6.jpg')
streaming_from_bag_file('./scaning_2/obj5.bag' ,'./output_2/new6.jpg' )
image2 = cv2.imread('./output_2/new6.jpg')
image_QR_detector1 , point_list1 = detect_qr_code(image1)
image_QR_detector2 , point_list2 = detect_qr_code(image2)

print(point_list1 ,point_list2)
