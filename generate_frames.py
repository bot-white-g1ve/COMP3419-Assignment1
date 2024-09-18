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

# 创建输出文件夹
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for frame_idx in range(0, min(1000, len(frames_blocks))):  # 确保不超出总帧数
    print(f'currently processing frame {frame_idx}')
    if frame_idx < len(frames_blocks) - 1:  # 确保有下一帧可用于映射
        mapping = find_best_match(frames_blocks, frame_idx)
        img_with_arrows = draw_arrow_in_frame(frames_blocks, frame_idx, mapping)
        # 保存带箭头的图像到文件
        cv2.imwrite(os.path.join(output_dir, f'frame_{frame_idx:03d}.png'), img_with_arrows)
    else:
        break

print("All frames have been processed and saved to the 'output' directory.")

