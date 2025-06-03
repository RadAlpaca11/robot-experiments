[Collected data](https://huggingface.co/datasets/RadAlpaca11/lerobotTests)

# Overall
We collect data using the Genesis simulator and output it as a .parquet file, which is the same format as lerobot datasets. The images are collected in a .zip file to make things neater and easier to download. The data is then uploaded to HuggingFace for easy access and sharing.

# Some notes on the code
* We use parallel simulation running on the GPU to move a single robot for each datapoint
* The code uses forward kinematics to move the robot joints to specific angles
* The points generated are in the range of the joints, but not necessarily in the range of the robot's workspace, so some of the positions may not be safe
    * The simulator does check for collisions, but that still doesn't mean the robot is in a safe position
* To keep the file names not too long, they only use the date, so they will write over one that has been done on the same day
* The code does take a while to run with more environments
    ![Environment number vs time](./envNums.png)
* The image .zip is not stored in the git repository, so you have to download it from [huggingface](https://huggingface.co/datasets/RadAlpaca11/lerobotTests)
* The .parquet file and the image .zip automatically get pushed to the [huggingface](https://huggingface.co/datasets/RadAlpaca11/lerobotTests) at the end of the code

# Plans
* Make the code more modular with functions and classes
* Create a safety check for the robot's workspace
