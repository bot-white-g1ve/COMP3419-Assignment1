import cv2
import os

output_dir = 'output'
image_files = sorted([os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.png')])

first_image = cv2.imread(image_files[0])
height, width, layers = first_image.shape

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_filename = 'output_video.avi'
video_out = cv2.VideoWriter(video_filename, fourcc, 30, (width, height))  # 30 FPS

for image_file in image_files:
    frame = cv2.imread(image_file)
    video_out.write(frame)

video_out.release()
cv2.destroyAllWindows()

print(f"Video created successfully and saved as {video_filename}")
