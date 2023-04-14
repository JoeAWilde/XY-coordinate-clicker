import cv2
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog

def get_click_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        param.append((x, y))

def get_video_file():
    root = tk.Tk()
    root.withdraw()
    video_file = filedialog.askopenfilename(title="Select a video file", filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.mov")])
    return video_file

video_file = get_video_file()
video = cv2.VideoCapture(video_file)
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
frame_ratio = int(input("Enter the frame ratio: "))

coordinates_df = pd.DataFrame(columns=["Frame", "Participant_ID", "X", "Y"])
window_name = "Video Frame"

for index in range(0, frame_count, frame_ratio):
    video.set(cv2.CAP_PROP_POS_FRAMES, index)
    ret, frame = video.read()
    if not ret:
        break

    clicks = []

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(window_name, get_click_coordinates, clicks)

    while True:
        for i, click in enumerate(clicks):
            cv2.circle(frame, click, 5, (0, 0, 255), -1)

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(0) & 0xFF

        if key == 32:  # 'space' pressed
            participant_id = simpledialog.askinteger("Participant ID", "Enter the participant ID:")
            if participant_id is not None:
                click_coordinates = clicks[-1]
                coordinates_df = coordinates_df.append({"Frame": index + 1, "Participant_ID": participant_id, "X": click_coordinates[0], "Y": click_coordinates[1]}, ignore_index=True)
            else:
                break
        elif key == 27:  # 'esc' pressed
            output_csv_path = os.path.join(os.path.dirname(video_file), 'coordinates.csv')
            coordinates_df.to_csv(output_csv_path, index=False)
            print(f"Output CSV file saved at: {output_csv_path}")
            cv2.destroyAllWindows()
            exit(0)

    cv2.setMouseCallback(window_name, lambda *args: None)  # Disable mouse callback for the next frame

cv2.destroyWindow(window_name)

output_csv_path = os.path.join(os.path.dirname(video_file), 'coordinates.csv')
coordinates_df.to_csv(output_csv_path, index=False)
print(f"Output CSV file saved at: {output_csv_path}")
