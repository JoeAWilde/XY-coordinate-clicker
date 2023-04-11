import os
import cv2
import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog


def select_video_file():
    root = tk.Tk()
    root.withdraw()
    video_file = filedialog.askopenfilename(title="Select video file", filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
    root.destroy()
    return video_file


def get_frame_ratio():
    root = tk.Tk()
    root.withdraw()
    frame_ratio = simpledialog.askinteger("Frame ratio", "Enter the frame ratio (e.g., 250 for 1 in every 250 frames):", minvalue=1)
    root.destroy()
    return frame_ratio


def get_frames(video_file, frame_ratio):
    frames = []
    vidcap = cv2.VideoCapture(video_file)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    for i in range(0, frame_count, frame_ratio):
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, i)
        success, frame = vidcap.read()
        if success:
            frames.append(frame)

    vidcap.release()
    return frames


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global click_coordinates
        click_coordinates = (x, y)
        cv2.circle(img, click_coordinates, 5, (0, 255, 0), -1)


video_file = select_video_file()
frame_ratio = get_frame_ratio()
frames_list = get_frames(video_file, frame_ratio)

click_coordinates = None
coordinates_df = pd.DataFrame(columns=["Frame", "X", "Y"])

for index, frame in enumerate(frames_list):
    img = frame.copy()
    window_name = f"Frame {index + 1}/{len(frames_list)}"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(window_name, mouse_callback)

    while True:
        cv2.imshow(window_name, img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord(" "):  # Spacebar pressed
            if click_coordinates:
                coordinates_df = coordinates_df.append({"Frame": index + 1, "X": click_coordinates[0], "Y": click_coordinates[1]}, ignore_index=True)
                coordinates_df.to_excel('coordinates.xlsx', index=False)
                click_coordinates = None
            break

        if key == ord("b"):  # 'b' pressed for going back
            if index > 0:
                index -= 2
                break

        if key == 27:  # 'esc' pressed
            cv2.destroyAllWindows()
            exit()

    cv2.destroyAllWindows()

coordinates_df.to_excel('coordinates.xlsx', index=False)
