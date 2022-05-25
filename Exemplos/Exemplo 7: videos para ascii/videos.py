
import numpy as np
from PIL import Image
import cv2
from pictures_to_ascii import get_ascii_color_from_raw_image,\
    get_ascii_grey_from_raw_image, get_ascii_text_from_raw_image,\
    xsize, ysize

video = cam = cv2.VideoCapture("data/Trackmania.mp4")
ascii_video = cv2.VideoWriter("data/Trackmania_ascii - color3.avi", 0, 60, (xsize, ysize))

# frame
currentframe = 0

while True:
    # reading from frame
    ret, frame = cam.read()

    if ret:
        image = Image.fromarray(frame)
        out = get_ascii_color_from_raw_image(image)
        ascii_video.write(np.array(out))
        currentframe += 1
        print(f"Frame {currentframe}")
        continue
    cv2.destroyAllWindows()
    video.release()
    break
