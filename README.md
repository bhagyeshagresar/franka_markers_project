# Group4 - Picking, placing, and cappings markers and caps

The goal of this project was to pick, place and cap markers with caps, and was thus heavily inspired by the application of robots in manufacturing and industry. Our project used a RealSense camera to detect colors of the markers, and MoveIt manipulation commands to actuate the robot. Franka-specific actions also were used to grip caps and markers during movement. The framework of the project was controlled using a state machine developed in the ROS package called SMACH. 

## Instructions to run the robot

The robot is run by issuing the following set of commands. To start, the user must connect to the Franka robot and enable ROS by activating the FCI.

The subsequent seuqence of steps are:
1) SSH into the robot using: 
`ssh -oSendEnv=ROS_MASTER_URI student@station`



2) Launch the the franka ros controller using the following command in the SSH terminal:
`roslaunch panda_moveit_config panda_control_moveit_rviz.launch launch_franka_control:=false robot_ip:=robot.franka.de`



3) Launch the robot manipulation and vision commands using the following launch file:
`roslaunch group4 launch_robot.launch`


4) Run the state machine to initiate the pick and place sequence using the following command:
`rosrun group4 TaskMaster`



## Subsystems 

### Manipulation

The manipulation

### Vision
#### Install OpenCV
* run the following command in a terminal: 
```shell
pip3 install opencv-python
```
#### vision python package
* All the computer vision algorithms are embeded in the `vision` python package, functions in the package can be called in a node by 
```import <package name>.<script name>``` such as 
```shell
import vision.vision1
```
* `sample_capture.py`:  A helper python script to capture images using realsense 435i rgbd camera
    1. Connect the realsense camera to you laptop
    2. Run the python script in a terminal:
    ```shell
    python3 sample_capture.py
    ```
    3. Press 'a' to capture and save an image and use 'q' to quit the image window
* `hsv_slider.py`: A helper python script to find the appropriate HSV range for color detection
    1. Add the path of the image to  `frame = cv.imread()` to read the image
    2. Run the python script in a terminal:
    ```shell
    python3 hsv_slider.py
    ```
    3. A window of original image and a window of HSV image with silde bars will show up
    4. Test with HSV slide bars to find an appropraite range
* `vision.py` A python script to detect contours and return list of hue values
    1. For testing purpose, an image can be loaded by setting the path to `image = cv.imread()`
    2. Run the python script in a terminal:
    ```shell
    python3 vision1.py
    ```
    3. A processed image with contours and a list of hue values will be returned

### SMACH
#### Installing and using SMACH-ROS
* run the following command in a terminal: `sudo apt-get install ros-noetic-smach ros-noetic-smach-ros ros-noetic-executive-smach ros-noetic-smach-viewer`
* smach is out of date and not maintained properly but most of the files can be fixed with a single key press.
#### Smach_viewer
* This package uses its own version of smach_viewer and is a node within the package.
#### Running Task master
* To run task master simply run: `rosrun group4 TaskMaster`

# Video demo
* The user interface of processed images and Franka arm visualizations on Rviz:   https://youtu.be/oCTd5CoBUqM
* The side view of the video record of Franka arm assembling the markers (3.0X faster): https://youtu.be/m37ZtrH2SsE
