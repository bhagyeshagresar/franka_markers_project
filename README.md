# Group4 - Picking, placing, and cappings markers and caps

The goal of this project was to pick, place and cap markers with caps, and was thus heavily inspired by the application of robots in manufacturing and industry. Our project used a RealSense camera to detect colors of the markers, and MoveIt manipulation commands to actuate the robot. Franka-specific actions also were used to grip caps and markers during movement. The framework of the project was controlled using a state machine developed in the ROS package called SMACH. Ensure that the panda_moveit_config and the franka_control packages are sourced and configured as detailed here: https://nu-msr.github.io/me495_site/franka.html


## Instructions to run the robot

The robot is run by issuing the following set of commands. To start, the user must connect to the Franka robot and enable ROS by activating the FCI.

The subsequent seuqence of steps are (first ensure a roscore is running, and you have configured your ROS_MASTER_URI appropriately):
1) SSH into the robot using: 
`ssh -oSendEnv=ROS_MASTER_URI student@station`

2) Launch the the franka ros controller using the following command in the SSH terminal:
`roslaunch panda_moveit_config panda_control_moveit_rviz.launch launch_franka_control:=false robot_ip:=robot.franka.de`


3) Up the collision limits for the robot by calling the following node and service:
`rosrun group4 limit_set`
`rosservice call /coll_hi`


4) Launch the robot manipulation and vision commands using the following launch file:
`roslaunch group4 launch_robot.launch`


5) Run the state machine to initiate the pick and place sequence using the following command:
`rosrun group4 TaskMaster`

## Instructions to run the rosinstall

Download and install the group4.rosinstall file to run the external packages used for this project:
`cd group4`
`vcs import src <path_to_rosinstall_file'.rosinstall>`

## Instructions to view the Sphinx Documentation of the Project

Open the `html` folder inside the `doc` directory using a web browser to view the Sphinx Documentation

### Automated Startup
Incase you want a faster startup method a bash script is set up which at least creates the terminals necessary for start up.
1) start by running the command: `bash sourceWS`
- This will source the workspace directory in your .bashrc
2) Run this command to begin: `bash start`
- This should start up every process to get the project started.  If it doesn't please refer to the section above.
3) When you are done using the start script run this command: `bash wsSourceRemove`
- This will remove the workspace from your .bashrc file, **only run once**.

## Subsystems 

### Manipulation

The manipulation package relies on several different nodes in order to function:
1) manipulation_cap provides low level position and orientation sensing services, along with error recovery, movements and gripper grasping
2) manipulation_macro_a provides position movement services for image captures using the realsense
3) manipulation_press provides a pressing service to cap the markers
4) manipulation_local provides manipulation services for moving in between trays
5) manipulation_pnp provides pick and place services between the feed and assembly trays
6) debug_manipulation logs the external forces experienced by the robot
7) plan_scene provides a planning scene for simulation based motion planning in Moveit
8) limit_set provides services to be used with the franka_control file launched prior to Moveit being launched. It allows the user to reconfigure the collision limits on the robot. 

Simulation with RVIZ can be run by running the following commands:
`roslaunch group4 planning_sim.launch`

Manipulation also relies on a python package called manipulation with translational, array position, and verification utilities.
A scene.yaml files is used for specifying parameters in the plan_scene node and the main manipulation movements scene elsewhere in the project.

### Vision
#### Install OpenCV
* run the following command in a terminal: 
```shell
pip3 install opencv-python
```
#### vision python package
* All the computer vision algorithms are embedded in the `vision` python package, functions in the package can be called in a node by 
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

    The node that uses this library is called vision_bridge.
* `vision_bridge node`: Node that publishes a stream of ROS Images and implements a service `capture` that returns a list of H values of the detected   markers and/or caps from an image.
    1. run `rosservice call /capture` and specify the `tray_location` to run the service.
        tray_location 1 : Represents Assembly Location
        tray_location 2 : Represents Markers Location
        tray_location 3 : Represents Caps Location

### SMACH

* If you are interested in editing or changing the behavior we encourage you take a look at SMACHs tutorial at: http://wiki.ros.org/smach. The state machine iterates between a series of states (Standby, Caps, Markers, genMatch, setTarget, Assemble). It relies on a manager package provided in source for sorting and matching. 

#### Installing and using SMACH-ROS
* run the following command in a terminal: `sudo apt-get install ros-noetic-smach ros-noetic-smach-ros ros-noetic-executive-smach`

#### Running Task master
* To run task master simply run: `rosrun group4 TaskMaster`

# Video demo
* The user interface of processed images and Franka arm visualizations on Rviz:   https://youtu.be/oCTd5CoBUqM
* The side view of the video record of Franka arm assembling the markers (3.0X faster): https://youtu.be/m37ZtrH2SsE
