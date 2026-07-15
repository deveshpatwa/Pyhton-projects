import ffmpeg 
import cv2
import subprocess

# importing video

video = cv2.VideoCapture("video_file.mkv")

print("video is opend") if video.isOpened() else print("There is some problem")


