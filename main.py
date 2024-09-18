import numpy as np
import math
import cv2

def load_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)  # Convert to grayscale for simplicity
    cap.release()
    return frames

def extract_blocks(frame, k):
    '''
    Return: blocks = [HEIGHT, WIDTH, BLOCK_SIZE, BLOCK_SIZE, RGB]
    '''
    fy, fx, channels = frame.shape
    block_size = 2 * k + 1
    # 计算横向和纵向可以完整划分的块数量
    num_blocks_y = fy // block_size
    num_blocks_x = fx // block_size
    # 创建一个三维数组来存储块
    blocks = np.zeros((num_blocks_y, num_blocks_x, block_size, block_size, channels), dtype=frame.dtype)
    
    for i, y in enumerate(range(0, fy - block_size + 1, block_size)):
        for j, x in enumerate(range(0, fx - block_size + 1, block_size)):
            blocks[i, j] = frame[y:y+block_size, x:x+block_size]
    
    return blocks

def process_video_frames(frames, k):
    """
    Return: [VIDEO_LEN, HEIGHT, WIDTH, BLOCK_SIZE, BLOCK_SIZE, RGB]
    """
    all_frames_blocks = []  # List to hold blocks from all frames

    for frame in frames:
        blocks = extract_blocks(frame, k)  # Extract blocks from the current frame
        all_frames_blocks.append(blocks)

    # Convert list of frames' blocks to a 5D NumPy array
    all_frames_blocks = np.array(all_frames_blocks)
    return all_frames_blocks

def calculate_ssd(block1, block2):
    # 计算差值
    diff = block1 - block2
    # 平方差
    squared_diff = np.square(diff)
    # 求和
    ssd = np.sum(squared_diff)
    # 开方
    root_ssd = np.sqrt(ssd)
    return root_ssd

ssd_min = 0
ssd_max = 1000
def is_valid_ssd(ssd):
    return ssd_min <= ssd <= ssd_max
def set_ssd_range(min_val, max_val):
    global ssd_min, ssd_max
    ssd_min = min_val
    ssd_max = max_val

search_range = 2
def find_best_match(frames_blocks, frame_idx):
    '''
    mapping: current frame each block's (y,x) -> corresponding block in next frame's (y,x)
    '''
    current_frame_blocks = frames_blocks[frame_idx]
    next_frame_blocks = frames_blocks[frame_idx + 1]
    height, width = current_frame_blocks.shape[:2]
    mapping = {}
    
    for y in range(height):
        for x in range(width):
            current_block = current_frame_blocks[y, x]
            min_ssd = float('inf')
            best_match = None  # Initialize best_match as None to handle invalid cases

            # Define search range within next frame's boundary
            for dy in range(-search_range, search_range+1):  # From -search_range to search_range
                for dx in range(-search_range, search_range+1):  # From -search_range to search_range
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < height and 0 <= nx < width:
                        candidate_block = next_frame_blocks[ny, nx]
                        ssd = calculate_ssd(current_block, candidate_block)
                        if ssd < min_ssd:
                            min_ssd = ssd
                            best_match = (ny, nx)

            # Check if the best_match is valid and the SSD is within valid range
            if best_match and is_valid_ssd(min_ssd):
                mapping[(y, x)] = best_match

    return mapping
def set_search_range(value):
    global search_range
    search_range = value

from helper_function import arrowdraw
def draw_arrow_in_frame(frames_blocks, frame_idx, mapping):
    # Reconstruct the full frame from blocks for the current frame
    # Extract dimensions
    _, height, width, block_height, block_width, rgb = frames_blocks.shape
    
    # Reconstruct the full frame from blocks for the current frame
    img = np.zeros((height * block_height, width * block_width, rgb), dtype=np.uint8)

    # Flatten the blocks into a full frame image
    for y in range(height):
        for x in range(width):
            start_y = y * block_height
            start_x = x * block_width
            img[start_y:start_y + block_height, start_x:start_x + block_width] = frames_blocks[frame_idx, y, x]

    # Draw arrows based on the mapping
    for (y, x), (ny, nx) in mapping.items():
        # Calculate the centers of the current and next blocks
        center_x = x * block_width + block_width // 2
        center_y = y * block_height + block_height // 2
        next_center_x = nx * block_width + block_width // 2
        next_center_y = ny * block_height + block_height // 2

        # Draw an arrow from the current block's center to the next block's center
        img = arrowdraw(img, center_x, center_y, next_center_x, next_center_y)

    return img