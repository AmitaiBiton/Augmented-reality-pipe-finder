import os
import tkinter as tk
from tkinter import simpledialog, ttk
from tkinter.messagebox import askyesno
import pyautogui as pag
import tkinter as tk
from tkinter import simpledialog
import cv2
from display_results import display
from pipe_detected_by_image_processing import get_pipe_with_color
from realSense_scaning import realsense_streaming
from streaming_from_bag_file import streaming_from_bag_file
from tracking_by_image_processing import LineTracking

def rooms_counter():
    ROOT = tk.Tk()
    ROOT.withdraw()
    # the input dialog
    USER_INP = simpledialog.askstring(title="Pipe Finder System2room",
                                      prompt="please enter counter of you rooms in house:")
    return USER_INP
def project_name():
    ROOT = tk.Tk()
    ROOT.withdraw()
    # the input dialog
    USER_INP = simpledialog.askstring(title="Pipe Finder System",
                                      prompt="Building new project  - please enter project name: ")
    return USER_INP
def room_name():
    ROOT = tk.Tk()
    ROOT.withdraw()
    # the input dialog
    USER_INP = simpledialog.askstring(title="Pipe Finder System",
                                      prompt="please enter room name:")
    if USER_INP == None:
        exit(0)

    return  str(USER_INP)
def create_room_record(rooms_counter ,folder_path):
    for i in range(int(rooms_counter)):
        room = room_name()
        path = folder_path + '/' + room
        if os.path.exists(path) == False:
            os.mkdir(path)
        else:
            while (os.path.exists(path)!=False):
                pag.alert(text="this room name:  "+ room +" is already exist  " , title=" room name")
                room = room_name()
                path = folder_path + '/' + room
                room = ""
            os.mkdir(path)

        realsense_streaming(str(path+'/'+ str(i+1)+ '.bag'))
        room = ""
def system_running(path1, path2):
    image1 = streaming_from_bag_file(path1)

    tracking = LineTracking(image1)
    tracking.processing()
    tracking.img_final = tracking.img_final[:, :, 0]
    # streaming_from_bag_file(path2)
    image2 = streaming_from_bag_file(path2)

    final_image = get_pipe_with_color(tracking, image2, image1)

    display(image2, path2)

if _name_ == '_main_':
    print("asas")
    project_name = project_name()
    if project_name == None:
        exit(0)
    folder_path = './'+project_name
    if os.path.exists(folder_path) == False:
        rooms_counter = rooms_counter()
        os.mkdir(folder_path)
        if rooms_counter == None:
            exit(0)
        create_room_record(rooms_counter ,folder_path)

    folder = './'+folder_path+''
    sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]

    cancel = False
    ROOT = tk.Tk()
    ROOT.withdraw()
    # the input dialog3
    USER_INP = simpledialog.askstring(title="Pipe Finder System",
                                      prompt="Choose room to scan second Scanning?\n"+ str(sub_folders))

    while USER_INP not in sub_folders:

        if USER_INP is None:
            print("cancel")
            cancel = True
            break

        else:
            result = pag.alert(text="Room is not exist!, please choose correct room!", title="Second Scan Alert")
            USER_INP = simpledialog.askstring(title="Pipe Finder System",
                                              prompt="Choose room number?\n" + str(sub_folders))

    if cancel == False: #not clicked on Cancel
        pag.alert(text="Starting second scan on room "+USER_INP,  title=" Start scan")
        path2 = str(folder+'/'+ USER_INP+'/'+ '2.bag')
        path1 = str(folder + '/' + USER_INP + '/' + '1.bag')
        realsense_streaming(path2)
        print("second scan just strated!") #just for check

        result = pag.confirm(text="Do you want a rescan room "+USER_INP+"?", title=" rescan room")
        while(result == 'OK'):
            print("second scan is starting on room " + USER_INP)
            result = pag.confirm(text="Do you want a rescan room " + USER_INP + "?", title=" rescan")

        pag.alert(text="Starting pipe finder calculation for room "+USER_INP,  title=" calculate ")
        if os.path.exists(str(folder+'/'+ USER_INP+'/'+ '2.bag')) and os.path.exists(str(folder+'/'+ USER_INP+'/'+ '1.bag')):
            system_running(path1 ,path2)
        result = pag.confirm(text="OK - continue to scan another rooms? \nCancel - exit the program", title=" scan another room")
        if result == 'OK':
            print("Choose room")
            USER_INP = simpledialog.askstring(title="Pipe Finder System",
                                              prompt="Choose room number?\n" + str(sub_folders))

            number_of_rooms = os.path
            folders = 0
            for _, dirnames, filenames in os.walk(folder):
                print("")

            if filenames == 2:  # 2 bag files
                result = pag.confirm(text="Do you want a override on scan of room " + USER_INP + "?", title=" scan again")

            print("override print")
        else:
            print("Exit")
            # call function to SEE RESULTS

    else:
        number_of_rooms = os.path
        folders = 0
        for _, dirnames, filenames in os.walk(folder_path):
            print("")