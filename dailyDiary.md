# 12/10/24
* What is ChatGPT: https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/

    * A paper that explains how LLMs and other types of machine learning work

# 12/17/24
* [Robot Dissection Notes](miscNotes/robotDissectionNotes.md)
    * We dissected a test robot to understand its systems and components with the plan to find a way to make the robots functional again.

# 12/19/24
* [CogACT Notes](miscNotes/CogACTnotes.md)
    * CogACT is a VLA architecture derived from VLM
* [OpenVLA Notes](openVLA/OpenVLAnotes.md)
    * OpenVLA is another VLA model, similar to CogACT
    * We have not yet been able to get this model running
* [Genesis Notes](genesis/genesisNotes.md)
    * Genesis is a universal physics engine developed entirely in python. It is lightweight, fast, and very user-friendly.

# 1/7/25
* [Agi Bot World Notes](miscNotes/AgiBotWorldNotes.md)
    * AgiBot World is a huge (in size and breakthrough) new open source robotics dataset.

# 1/9/25
* Updated and organized repository and notes
* worked on gettingCogACT to work
    * Discovered that it needs a server-class machine to run
* got AgiBot World visualization to work

# 1/14/25
* Worked to get CogACT to work on server-class machine
    * ran out of storage on the server
* worked on getting OpenVLA to work

# 1/16/25
* continued working on CogACT after clearing storage
* Got CogACT to work on server-class machine 
* Got OpenVLA to work
* integrated openVLA with Genesis

# 1/21/25
* began working on mujoco playground

# 1/23/25
* got mujoco playground ai to work
* tried to access rgb render with genesis to continue working on integrating openVLA and genesis

# 1/28/25
* got IsaacSim to work
* got openvla and genesis integrated with inverse kinematics (not fully successful yet)

# 1/30/25
* worked on getting openPi0 to work
* got openVLA and genesis successfully integrated! 
    * [video](openVLA/picsAndVids/film.mp4)

# 2/4/25
* Did a bit of research on deepseek
* worked on getting openPi0 to work
* worked on isaacsim
    * began exploring the scripting capabilities

# 2/6/25
* worked on getting genesis working on server
    * plans to integrate cogACT and genesis in the future
* began working on getting the official pi0 to work
* got pi0 to work!
    * It was not easy. The example code sucked!

# 2/11/25
* Ran into some issues with connecting to servers
* Began looking into docker and dev containers for vscode
* Researched quaternions to understand VLA outputs

# 2/25/25
* Looked into using xARM with genesis
* Looked into magma


# 2/27/25
* Got magma running
    * not with actions just observations

# 3/11/25
* worked with openvla-oft 
    * able to get outputs, unsuccessful with our own inputs so far

# 3/13/25
* continued working on openvla-oft 
* explored [magma robot demo](magma/magmaSource/agents/robot_traj/app.py)
    * This is not great yet, it only really draws random lines

# 3/20/25
* worked on getting openvla to work so we could use it for the kuka arm, but it wasn't working and being weird
    * It wanted us to install vla, which is not a thing
* began using [Issac-GR00T](Isaac-GR00T), getting it installed and through the inference example code in the [getting_started](Isaac-GR00T/getting_started/) folder

# 4/1/25
* worked on openvla-oft on server
    * cuda devices not working. I believe this is because it has a version of cuda that it can't handle?
* worked on getting octo up and running
* experimented with magma
    * currently none of the agents are working for some reason
    * ValueError: When localhost is not accessible, a shareable link must be created. Please set share=True or check your proxy settings to allow access to localhost.
    * even when we do this and open the site we get: Internal Server Error
    * Other errors in the terminal as well: TypeError: argument of type 'bool' is not iterable

# 4/8/25
* Worked on integrating magma with genesis
    * [notes](magma/magmaNotes.md)
    * [code](magma/magmaGen.py)
    * Able to integrate, but not perform successfully. The output actions are quite large numbers and we are struggling to understand how to interpret them in our code.
* Created a table of the robot arms in the lab, models if we have them, and the status if we've worked on them [file](robots.md)

# 4/10/25
* worked on integrating magma with genesis
* looked at xarm movement code, and made sure it still worked
* got [xarm urdf](ManiSkill-XArm6/xarm6_robotiq.urdf) loaded with ``` gs view models/ManiSkill-XArm6/xarm6_robotiq.urdf```
* worked on [xarm6MagmaGen.py](magma/xarm6MagmaGen.py)
    * we increased the mass of the base from 2.6 to 20.6 so that the arm would not topple over
    * joint control now works, but not through inverse kinematics yet
    * inverse kinematics seems to move the robot as a whole, not the joints

# 4/22/25
[code](magma/xarm6MagmaGen.py)
[video](magma/video1.mp4)
* Worked on getting xArm6 working with genesis. The issue was inverse kinematics not working with the arm in genesis. We figured it would work if we called the xarm api, and used that inverse kinematics. Later I wrote code that makes a 'digital twin' of the xarm in the lab. I went and moved the xarm around while it was in mode 2, and then genesis would control the robot in the simulator to do the same thing.
    * The physical arm in the lab is raised up, so the base (which all coordinates are based off of) is off of the table a bit, so sometimes the simulation arm would drag on the ground
    * We could potentially add a platform to the urdf file to have a completely accurate model in the simulator

# 4/24/25
* [Added a box for the xarm to stand on](models/ManiSkill-XArm6/mod_xarm6_nogripper.urdf), so that it would be more accurate to the lab
* got [xarm integrated with magma and genesis](magma/xarm6MagmaGen.py)

# 4/29/25
* [Updated camera view for xarm](magma/xarm6GenesisData.py)
* updated method of taking [pictures with genesis](magma/xarm6GenesisData.py)
```python
output = cam.render()
imageData = output[0]
frame = cv2.cvtColor(imageData, cv2.COLOR_BGR2RGB)
cv2.imwrite('frame.jpg', frame)
```
* began working on [code to generate points in space for robot](magma/distributionTest.py)

# 5/1/25
* Updated [distribution code](magma/distributionTest.py)
* remembered that we needed to use radians
* Tested code with simulation
* Modified [robot model with hand](models/ManiSkill-XArm6/mod_xarm6_robotiq.urdf)
* Tested [code with robot with hand](magma/xarm6GenesisData.py)

# 5/6/25
* added frame capture to [xarm and genesis code](magma/xarm6GenesisData.py) with the hope of this helping with data collection later
* researched [lerobot](miscNotes/lerobotNotes.md) data collection
    * started working on adapting code to work with genesis
* found a potentially helpful (genesis and lerobot source)[https://github.com/alexis779/slobot]
* turned on collision in [xarm with genesis](magma/xarm6Genesis.py)

# 5/8/25
* added to [xarm genesis code](magma/xarm6Genesis.py) to be able to generate a lerobot-formatted [dataset](magma/lerobotTests/robotDataTest.parquet) and uploaded it to [HuggingFace](RadAlpaca11/lerobotTests) to see if it looked like others, which it did.