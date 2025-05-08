# Notes
In genesis we made a [test dataset](RadAlpaca11/lerobotTests)


## Main structure of a dataset (taken from the README)
```
dataset attributes:
  ├ hf_dataset: a Hugging Face dataset (backed by Arrow/parquet). Typical features example:
  │  ├ observation.images.cam_high (VideoFrame):
  │  │   VideoFrame = {'path': path to a mp4 video, 'timestamp' (float32): timestamp in the video}
  │  ├ observation.state (list of float32): position of an arm joints (for instance)
  │  ... (more observations)
  │  ├ action (list of float32): goal position of an arm joints (for instance)
  │  ├ episode_index (int64): index of the episode for this sample
  │  ├ frame_index (int64): index of the frame for this sample in the episode ; starts at 0 for each episode
  │  ├ timestamp (float32): timestamp in the episode
  │  ├ next.done (bool): indicates the end of an episode ; True for the last frame in each episode
  │  └ index (int64): general index in the whole dataset
  ├ episode_data_index: contains 2 tensors with the start and end indices of each episode
  │  ├ from (1D int64 tensor): first frame index for each episode — shape (num episodes,) starts with 0
  │  └ to: (1D int64 tensor): last frame index for each episode — shape (num episodes,)
  ├ stats: a dictionary of statistics (max, mean, min, std) for each feature in the dataset, for instance
  │  ├ observation.images.cam_high: {'max': tensor with same number of dimensions (e.g. `(c, 1, 1)` for images, `(c,)` for states), etc.}
  │  ...
  ├ info: a dictionary of metadata on the dataset
  │  ├ codebase_version (str): this is to keep track of the codebase version the dataset was created with
  │  ├ fps (float): frame per second the dataset is recorded/synchronized to
  │  ├ video (bool): indicates if frames are encoded in mp4 video files to save space or stored as png files
  │  └ encoding (dict): if video, this documents the main options that were used with ffmpeg to encode the videos
  ├ videos_dir (Path): where the mp4 videos or png images are stored/accessed
  └ camera_keys (list of string): the keys to access camera features in the item returned by the dataset (e.g. `["observation.images.cam_high", ...]`)
```

# The plan
* we may need to modify the @safe_disconnect decorator for the simulation
* we will likely have to adapt almost all of the code to work with the simulator
* data to take
    * observation state
        * recorded joint positions
    * action
        * positions we gave the robot (having this and observation state will help when the robot collides with itself in simulation, so we could make sure it doesnt do that in the future. We could also potentially use the xarm SDK to check the positions)
    * image
        * the frame of simulation 
    * timestamp
        * the timestamp
    * frame_index
        * the number of the frame
    * episode_index
        * number of the episode
    * index
        * same as frame?
    * task_index
        * same as episode? Unless we come back to certain positions later, so we can keep the same key of that location

* We could also record the forward kinematics, getting the real coordinates if we want

* 

python lerobot/scripts/control_robot.py \
  --robot.type=xarm6 \
  --control.type=record \
  --control.fps=30 \
  --control.single_task="Go to the given joint positions" \
  --control.repo_id=${HF_USER}/xarm6Test \
  --control.tags='["xarm6","genesis"]' \
  --control.warmup_time_s=5 \
  --control.episode_time_s=30 \
  --control.reset_time_s=30 \
  --control.num_episodes=2 \
  --control.push_to_hub=true



https://github.com/alexis779/slobot