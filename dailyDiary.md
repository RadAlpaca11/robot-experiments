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
