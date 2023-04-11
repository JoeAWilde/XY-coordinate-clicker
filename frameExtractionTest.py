# Importing all necessary libraries
import cv2
import os
  
net = 'net9'

if os.path.exists('F:/'):
    dir_prefix = 'F:/OneDrive - University of Exeter/Crab videos/waveMorpho/' + net + '/frames/'
else:
    dir_prefix = 'C:/Users/jw777/OneDrive - University of Exeter/Crab videos/waveMorpho/' + net + '/frames/'

# Read the video from specified path, needs changing for every net
cam = cv2.VideoCapture(r"C:\Users\jw777\OneDrive - University of Exeter\Crab videos\SKD videos\Network vids\Network 9 01-06-2011\20110601\20110601_101719.m2ts") 

try:
      
    # creating a folder named data
    if not os.path.exists(dir_prefix + 'real frames'):
        os.makedirs(dir_prefix + 'real frames')
  
# if not created then raise error
except OSError:
    print ('Error: Creating directory of data')
  
# frame
currentframe = 0
  
while(True):
      
    # reading from frame
    ret,frame = cam.read()
  
    if ret:
        # writing the extracted image
        if currentframe % 250 == 0:
            name = dir_prefix + 'real frames/' +  str(currentframe) + '.jpeg'
            print ('Creating...' + name)
            cv2.imwrite(name, frame)
  
        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1
    else:
        break
  
# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()