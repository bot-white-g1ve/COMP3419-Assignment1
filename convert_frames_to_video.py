import cv2
import os

# 输出目录和文件格式
output_dir = 'output'
image_files = sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.png')])

# 读取第一张图像来获取视频的尺寸
first_image = cv2.imread(image_files[0])
height, width, layers = first_image.shape

# 设置视频编码器和视频输出参数
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用XVID编码器
video_filename = 'output_video.avi'
video_out = cv2.VideoWriter(video_filename, fourcc, 30, (width, height))  # 30 FPS

# 遍历所有图像文件，将它们作为帧写入视频
for image_file in image_files:
    frame = cv2.imread(image_file)
    video_out.write(frame)  # 写入帧

# 释放视频写入器和销毁所有窗口
video_out.release()
cv2.destroyAllWindows()

print(f"Video created successfully and saved as {video_filename}")
