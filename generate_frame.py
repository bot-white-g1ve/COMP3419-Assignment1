import cv2
import numpy as np
from main import *
import os
import yaml
import argparse

parser = argparse.ArgumentParser(description="Load a YAML configuration file.")
parser.add_argument('config', type=str, help="Path to the configuration file.")
args = parser.parse_args()

with open(args.config, 'r') as file:
    config = yaml.safe_load(file)

video_path = 'monkey/monkey.avi'
k = config['k']  # Block size
set_ssd_range(config['ssd_min'], config['ssd_max'])
set_search_range(config['search_range'])

frames = load_video_frames(video_path)  # Load video frames
frames_blocks = process_video_frames(frames, k)  # Process frames to blocks
print(f"Extracted frames blocks shape: {frames_blocks.shape}")
frame_idx = 86
mapping = find_best_match(frames_blocks, frame_idx)
img_with_arrows = draw_arrow_in_frame(frames_blocks, frame_idx, mapping)
cv2.imshow("Frame with Motion Arrows", img_with_arrows)
cv2.waitKey(0)
if frame_idx + 1 < len(frames):
    next_frame_img = frames[frame_idx + 1]
    cv2.imshow("Next Frame", next_frame_img)
    cv2.waitKey(0)
cv2.destroyAllWindows()