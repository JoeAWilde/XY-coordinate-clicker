import cv2
import os
import imageio
from moviepy.editor import *

net = 'net14'

if os.path.exists('F:/'):
    dir_prefix = 'F:/OneDrive - University of Exeter/Crab videos/waveMorpho/' + net + '/frames/'
else:
    dir_prefix = 'C:/Users/jw777/OneDrive - University of Exeter/Crab videos/waveMorpho/' + net + '/frames/'

try:
    if not os.path.exists(dir_prefix + 'metre stick frames/'):
        os.makedirs(dir_prefix + 'metre stick frames/')
except:
    print("OS Error: cannot create file")

dir_prefix = dir_prefix + 'metre stick frames/'

video_path_prefix = r"D:\SKD videos\2011 Uca Networks\Network 14 04-06-2011\20110605"
video_file = r"\20110604_122707(4)"

video_path = video_path_prefix + video_file + r".m2ts"
converted_video_path = video_path_prefix + video_file + r"_converted.mp4"

if not os.path.isfile(converted_video_path):
    # Convert the video to MP4 format
    clip = VideoFileClip(video_path)
    clip.write_videofile(converted_video_path, codec='libx264', audio_codec='aac')

# Replace the original video path with the converted video path
video_path = converted_video_path

cam = cv2.VideoCapture(video_path)

fps = int(cam.get(cv2.CAP_PROP_FPS))
interval = fps
start_time = (9 * 60) + 25
start_frame = start_time * fps
total_frames = 60

current_frame = 0
extracted_frames = 0

cam.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

while True:
    ret, frame = cam.read()

    if ret:
        current_frame = int(cam.get(cv2.CAP_PROP_POS_FRAMES))
        if current_frame >= start_frame and extracted_frames < total_frames:
            if (current_frame - start_frame) % interval == 0:
                timestamp_sec = current_frame / fps
                timestamp_min_sec = f'{int(timestamp_sec // 60)}:{int(timestamp_sec % 60)}'
                name = dir_prefix + f'{timestamp_min_sec.replace(":", "-")}.jpeg'
                print(f'Creating {name} at {timestamp_min_sec} (min:sec)')
                cv2.imwrite(name, frame)
                extracted_frames += 1
    else:
        break

    if extracted_frames == total_frames:
        break

cam.release()
cv2.destroyAllWindows()
