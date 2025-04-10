#!/usr/bin/env python3
import time
from xarm import XArmAPI


# Initialize the robot.
def initialize_robot(arm):
    arm.clean_warn()
    arm.clean_error()
    arm.motion_enable(True)
    arm.set_mode(0)
    arm.set_state(0)
    arm.move_gohome(wait=True)

def main():
    # Replace with the actual IP address of your xArm
    arm_ip = '172.20.5.100'
    
    # Initialize the xArm API
    arm = XArmAPI(arm_ip)
    time.sleep(1)  # Waiting for connection to be established

    initialize_robot(arm)
    arm.set_mode(2)
    arm.set_state(0)

    print("xArm is ready. Manually move the arm to the desired point.")
    input("Press Enter after reaching the target position...")

    # Record the current end effector position
    position = arm.get_position()
    print("Recorded end effector position:", position)
    
    # Disconnect from the arm
    arm.disconnect()

if __name__ == "__main__":
    main()