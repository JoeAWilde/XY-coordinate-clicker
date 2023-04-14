import os
import cv2
import numpy as np
import pandas as pd
import keyboard

# Function to handle mouse click events
def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if the current frame already has a coordinate
        existing_coordinates = [coord for coord in coordinates if coord[0] == current_frame]

        # If there are existing coordinates for the current frame, update the last one
        if existing_coordinates:
            last_coord_index = coordinates.index(existing_coordinates[-1])
            coordinates[last_coord_index] = (current_frame, x, y)
        # If there are no existing coordinates for the current frame, append a new one
        else:
            coordinates.append((current_frame, x, y))

        # Draw a tick mark on the frame
        cv2.line(frame, (x - 10, y - 10), (x, y), (0, 255, 0), 2)
        cv2.line(frame, (x, y), (x + 10, y - 10), (0, 255, 0), 2)
        cv2.imshow('Frame', frame)

# Set the directory path containing the frames
net = "net14"

if os.path.exists('F:/'):
    frames_directory = 'F:/OneDrive - University of Exeter/Crab videos/waveMorpho/' + net + '/frames/real frames/female_frames'
else:
    frames_directory = 'C:/Users/jw777/OneDrive - University of Exeter/Crab videos/waveMorpho/' + net + '/frames/real frames/female_frames'

#Set the working directory ####
os.chdir(frames_directory)

# Sort the frame filenames
frames_list = sorted([f for f in os.listdir(frames_directory) if f.lower().endswith('.jpeg')])
total_frames = len(frames_list)

# Set up mouse callback
coordinates = []
current_frame = ''
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback('Frame', on_mouse_click)

# Initialize other variables
excel_file = net + 'coordinates.xlsx'
index = 0

# Load existing coordinates from Excel file, if it exists
excel_file = net + 'coordinates.xlsx'
if os.path.exists(excel_file):
    coordinates_df = pd.read_excel(excel_file)
    # If the data frame is empty
    if not coordinates_df.empty:
        coordinates = coordinates_df.values.tolist()
        # Go to the final row as the frame that was last processed
        last_processed_frame = coordinates[-1][0]
        index = frames_list.index(last_processed_frame) + 1
    else:
        coordinates = []
else:
    coordinates_df = pd.DataFrame(columns=['Frame', 'X', 'Y'])
    coordinates = []

while index < total_frames:
    frame_filename = frames_list[index]
    frame_path = os.path.join(frames_directory, frame_filename)
    frame = cv2.imread(frame_path)

    if frame is None:
        print(f"Error: Could not open frame {frame_filename}.")
        index += 1
        continue

    current_frame = frame_filename

    # Add progress text to the frame
    progress_text = f"Frame {index + 1}/{total_frames}"
    cv2.putText(frame, progress_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Frame', frame)

   # Wait for space bar press, ESC key, or backspace key
    while True:
        if keyboard.is_pressed('space'):
            # Save coordinates to Excel spreadsheet
            coordinates_df = pd.DataFrame(coordinates, columns=['Frame', 'X', 'Y'])
            coordinates_df.to_excel(excel_file, index=False)
            cv2.waitKey(100)  # Add a small delay after pressing the spacebar
            index += 1
            break
        if keyboard.is_pressed('esc'):
            # Save coordinates to Excel spreadsheet
            coordinates_df = pd.DataFrame(coordinates, columns=['Frame', 'X', 'Y'])
            coordinates_df.to_excel(excel_file, index=False)
            cv2.destroyAllWindows()
            exit()
        if keyboard.is_pressed('backspace'):
            # Remove clicks related to the current frame
            coordinates = [coord for coord in coordinates if coord[0] != current_frame]
            coordinates_df = pd.DataFrame(coordinates, columns=['Frame', 'X', 'Y'])  # Update the coordinates_df DataFrame
            coordinates_df.to_excel(excel_file, index=False)  # Save the updated DataFrame to the Excel file
            index = max(index - 1, 0)
            cv2.waitKey(100)  # Add a small delay after pressing the backspace key
            break
        cv2.waitKey(1)

# Close all windows
cv2.destroyAllWindows()