import cv2
import os

net = 'net2'

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

cam = cv2.VideoCapture(r"E:\SKD videos\2011 Uca Networks\Network 3 21-05-2011\20110521\20110521_120719.m2ts")

fps = int(cam.get(cv2.CAP_PROP_FPS))
interval = fps
start_time = (4 * 60) + 20
start_frame = start_time * fps
total_frames = 10

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
