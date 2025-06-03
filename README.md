[Daily diary](dailyDiary.md): This is a log of our work and progress.

[Tasks](tasks.md): This is a list of tasks that we are working on or need to work on.

[Robots](robots.md): This is a table of the robots in the lab, with their models and status of what we have worked on.

[Troubleshooting](troubleshooting.md): This is a list of common issues we run into and how we solve them.


# File structure
> **General conventions**:
> - picsAndVids appears in multiple folders, an is a collection of pictures and videos taken using the project. (not specified in the file structure)
> - Notes that are related to a project that we have an organized folder dedicated to are in that folder.
* [miscNotes](miscNotes): Notes on topics that do not fit into other folders or are not related to a specific project
* [genesis](genesis): Overall folder for Genesis work. The work in this folder is focused on the simulator by itself. The work integrating the simulator with openVLA is in the openVLA folder.
    * [graveyard](genesis/graveyard): Old code that we haven't tested and are no longer using
    * [mujoco_menagerie](genesis/mujoco_menagerie): A collection of mjcf models that we use in genesis
    * [tested](genesis/tested): Code that we have tested and confirm works. Sometimes this code needs to be slightly modified to fit the path of the model and will put pictures and videos in different places, but it works.
* [openVLA](openVLA): Overall folder for openVLA work. The main work in this folder is integrating openVLA with Genesis
    * [openvlaSource](openVLA/openvlaSource): Source code for openVLA
* [mujocoPlayground](mujocoPlayground): Overall folder for mujoco playground work. The folder currently mainly contains jupyter notebooks that are from the website, that we have slightly modified to learn how the software works.
    * [mujocoTutorials](mujocoPlayground/mujocoTutorials): Tutorials from the mujoco playground website
* [openPi0](openPi0): Overall folder for openPi0 work.
* [openPi](openPi): Overall folder for openPi work.
* [openvla-oft](openvlaOFT/openvla-oft): Overall folder for openvla-oft work.
* [magma](magma): Folder of Magma work. This also includes code for data collection that we are planning to use to finetune the model.
    * [magmaSource](magma/magmaSource): The source code for magma (this is a submodule so you may have to pull it separately)
* [Isaac-GROOT](Isaac-GR00T): source code for Isaac-GR00T



# Links
* [What is ChatGPT](https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/): An article we read to learn about how LLMs and other types of machine learning work
* [Robot Dissection Notes](miscNotes/robotDissectionNotes.md): Notes from when we dissected a test robot to understand its systems and components with the plan to find a way to make the robots functional again.
* [CogACT Notes](miscNotes/CogACTnotes.md): Notes on CogACT, a VLA architecture derived from VLM
* [OpenVLA Notes](openVLA/OpenVLAnotes.md): Notes on OpenVLA, a VLA model that we have gotten working with genesis simulator.
* [Genesis Notes](genesis/genesisNotes.md): Notes on Genesis World, a physics simulator
* [Agi Bot World Notes](miscNotes/AgiBotWorldNotes.md): Notes on AgiBot World, a new and large open source robot dataset
* [Omniverse Notes](miscNotes/omniverseNotes.md): Notes on omniverse, a simulator we are experimenting with
* [Mujoco Playground Notes](mujocoPlayground/mujocoPlaygroundNotes.md): Notes on mujoco playground, another simulator that we are learning how to utilize
* [Pi0 Notes](openPi0/pi0Notes.md): Notes on openPi0, an open source vla that is based on a paper describing a VLA
* [Magma Notes](magma/magmaNotes.md): notes on magma and a guide to get it working

