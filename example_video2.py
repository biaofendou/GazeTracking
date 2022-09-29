"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import cv2
from gaze_tracking import GazeTracking
import time
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
import numpy as np
import datetime

# gaze_num = 0
gaze = GazeTracking()
webcam = cv2.VideoCapture("xiang.mp4")
# video = cv2.VideoCapture("xiang.mp4")
out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc("m", "p", "4", "v"), 30, (640, 432))

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()
    # _, frame1 = video.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""
    global gaze_num
    if gaze.is_center():
        gaze_num = 0
        text = "视线正常"
    else:
        gaze_num += 1
        if gaze_num >= 60:
            text = "有作弊嫌疑"
        else:
            text = "视线异常"

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype("simfang.ttf", 24, encoding="utf-8")

    if text == "视线正常":
        color = (0,255,0)
    elif text == "视线异常":
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)
    draw.text((90, 60), text, color, font=fontText)
    draw.text((90, 130), "左眼位置:  " + str(left_pupil), cv2.FONT_HERSHEY_DUPLEX, font=fontText)
    draw.text((90, 165), "右眼位置:  " + str(left_pupil), cv2.FONT_HERSHEY_DUPLEX, font=fontText)
    frame = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2RGB)
    out.write(frame)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break

webcam.release()
out.release()
cv2.destroyAllWindows()
