import tkinter as tk
from tkinter import simpledialog
import cv2

from display_results import display
from pipe_detected_by_image_processing import get_pipe_with_color
from streaming_from_bag_file import streaming_from_bag_file
from tracking_by_image_processing import LineTracking

"""
ROOT = tk.Tk()
ROOT.withdraw()
# the input dialog
USER_INP_file = simpledialog.askstring(title="Test",
                                  prompt="please enter file name:")
print(USER_INP_file)
USER_INP_scan_number= simpledialog.askstring(title="Test",
                                  prompt="for scan one enter 1 for scan to enter 2")

print(type(USER_INP_scan_number))
USER_INP_scan_number =int(USER_INP_scan_number)
print(type(USER_INP_scan_number))


while int(USER_INP_scan_number) != 1 or int(USER_INP_scan_number) != 2:
    USER_INP_scan_number = simpledialog.askstring(title="Test",
                                                  prompt="for scan one enter 1 for scan to enter 2")

"""


# realsense scaning first

image1 = streaming_from_bag_file('./scaning/obj5.bag')

tracking = LineTracking(image1)
tracking.processing()
tracking.img_final = tracking.img_final[:, :, 0]

# realsense scaning two

image2 = streaming_from_bag_file('./scaning_2/obj5.bag')

final_image = get_pipe_with_color(tracking, image2, image1)

display(image2,'./scaning_2/obj5.bag')

