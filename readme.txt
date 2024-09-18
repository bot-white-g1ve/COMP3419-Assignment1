# How to run the program
1. Write a config or use the default configs. The recommended one is 'configs/k4_ssd130-135_sr3.yaml'
2. Run `python generate_frames.py configs/k4_ssd130-135_sr3.yaml`. This will generate all the frame images and put them in 'output' directory
3. Run `python convert_frames_to_video.py`. This will convert all the frame images in 'output' directory into a video

# Configs
k: the block size
ssd_min and ssd_max: the minimum ssd and the maximum ssd (ssd out of the range are considered invalid)
search_range: the search range (how many blocks to search in the next frame to determine the best match)

# Experiments
The experiments are recorded in experiments.txt

# Final outcome
k = 4, ssd = (130, 135), search_range = 3
please see "videos/k4_ssd130-135_sr3.avi"