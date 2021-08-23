# Augmented-reality-pipe-finder

### build a system that can display the pipes inside the wall:
![alt text](https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/master/Images/git1.png)  

The system uses a 3D camera on packets to scan the wall when the pipes are exposed 
during construction, and another scan when construction is complete,
the first scan result we impose on the second scan and present to the customer.



#### Scan by Intel® RealSense™ Depth Cameras
To activate the camera we used Intel's SDK to scan and save the relevant data.
It is important to note that the camera has two types of images,
the first is a standard color image with a resolution of 1920 X 1080.  
the second image is the depth image in which by building the right software you can get in each pixel and pixel the distance from the object taken
![alt text](https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/master/Images/depth.png)  

#### Filters on Depth image
The camera, like any other hardware component,
has a certain limitation, 
this limitation is mainly reflected in the depth calculation for each pixel and pixel in the image
since there are close to 2 million pixels the camera fails to cover everything and there are 
lots of areas defined as black where the distance Use certain filters to complete the information.
One of the filters we used is:  

##### Spatial:
This filter knows how to complete mainly information in complex areas where there 
are small holes in the middle of the image and the completion is performed by calculating values in close pixels in the image.
![alt text](https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/master/Images/spatial.png)  


##### Resolutions Processes:
In order to match the resolutions in the depth image compared to the color image 
there is a function from the SDK that performs a stretch when after the stretch we will have to perform the process of the filters again in order to complete the missing information.


#### Detection the pipes from scan 1:
Using algorithms and functions from the CV2 library to identify and capture the tubes on the color image.
![alt text](https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/master/Images/detection.png)  

It is important to note that since we use image processing algorithms the results are not 100% of detection and perception 
so further research on neural networks and deep learning has been done Link to additional project - https://github.com/AmitaiBiton/cable_and_wire_finder


#### QR Detection:
In order to match two different angles of photography scanned in the two different
blanks 4 unique values must be identified in the two scans that indicate the same place in the real world
even though their value is different in relation to the displayed image,
so the user was required to hang QR on both scans. Unique QR edges are more detailed in the relevant section.
![alt text](https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/master/Images/QR.png) 

#### calculate the distance pipe to the wall or between pipes:
![alt text](https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/master/Images/3D_distance.png) 

##### step one see the check the depth camera:
we need to check some points and see the different exampale:  
It can be seen that the point on the pipe is closer, the value is calculated in millimeters.  


![alt text](https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/master/Images/depth_point.png)   
      
      
##### step two check the convert function from 2D pixel to 3D points:
to calculate the distance between two objects we need the 3D points of the two objects so we need to convert the image from 2D to 3D image.  
exampale:  
pixel - (u,v)   
point - (X,Y,Z)  

![alt text](https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/master/Images/2D_to_3D.png)   

### localization step - is about to Match the two different scans by rotating in three dimensions:  
In order for us to perform the round, it is necessary to identify 4 points  
in real space in the two different scans, from these four points  
we can build a matrix for each scan when there is one missing matrix that expresses the transition between the matrix from the first scan and the second scan.  
2D taken convert them to 3D and perform the desired rotation we need in order to match the two scans and cast the information correctly.
see - https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/main/code/detect_Qr_code.py - find points.  

see - https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/main/code/localization_processes.py




## Results:
The system will allow the user to make two options:
1. Calculate distances between 2 objects in the image shown in the example below so that, for example,  
  the user can know the position of the pipe in relation to the left or right wall.
  
  ![alt text](https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/master/Images/output1.png)   

  
3. The user will be able to mark in advance before the second emptying where he wants to perform a drilling operation for the purpose and then according to when the system will lay the pipes in relation to the last scan he performed, if the marking meets a pipe then he will not be able to perform the same operation in this area.

![alt text](https://github.com/AmitaiBiton/Augmented-reality-pipe-finder/blob/master/Images/mark.png)   
