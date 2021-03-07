#!/usr/bin/python3

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# hough line detector with cv2
def findColorAndLine(hsv, frame, markerColors):
	for idxColor, color in enumerate(markerColors):
		lower = np.array(color[0:3])
		upper = np.array(color[3:6])
		mask = cv2.inRange(hsv, lower, upper)
		edges_line = cv2.Canny(mask, 75, 150)
		lines = cv2.HoughLinesP(edges_line, 1, np.pi/180, 50, maxLineGap=50)
		if lines is not None:
			for line in lines:
				x1, y1, x2, y2 = line[0]
				cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
				if y2 < y1: 
					trail_points[idxColor].appendleft((int(x2) , int(y2)))
				else:
					trail_points[idxColor].appendleft((int(x1), int(y1)))

# hough circles with cv2
def findBall(hsv, ballMin, ballMax, pts_ball):
	tennis_mask = cv2.inRange(hsv, ballMin, ballMax)
	tennis_mask = cv2.dilate(tennis_mask, None, iterations=2)
	tennis_mask = cv2.erode(tennis_mask, None, iterations=2)
	ball_edges = cv2.Canny(tennis_mask, 75, 150)
	size = tennis_mask.shape
	h, s = 0.0, 0.0
	ball_circles = cv2.HoughCircles(ball_edges, cv2.HOUGH_GRADIENT, 1,
	80, param1=50, param2=10, minRadius=20, maxRadius=50)
	if ball_circles is not None:
		ball_circles = np.uint16(np.around(ball_circles))
		for circle in ball_circles[0, :]:
			for m in range(-30, 30):
				for n in range(-30, 30):
					if 0 <= (circle[1] + m) < size[0] and 0 <= (circle[0] + n) < size[1]:
						h += tennis_mask[circle[1]+m, circle[0]+n]
						s += 1
			if h / s > 215 and circle[2] > 20:
				cv2.circle(frame, (int(circle[0]), int(circle[1])), int(circle[2]), (255, 0, 0), 2)
				center = (int(circle[0]), int(circle[1]))
				pts_ball.appendleft(center)
	return ball_edges


ballMin = np.array([18, 64, 57])
ballMax = np.array([40, 255, 255])

""" Change the values according to the mask created by "color_detector" file in the following order:
	Hue min, Sat min, Val min, Hue max, Sat max, Val max.
	In my case, the first is the value of orange and the second is blue."""

markerColors = [[0, 29, 250, 43, 255, 255],  
				[50, 170, 186, 255, 255, 255]] # orange, blue
myColors = [[0, 165, 255], [255, 165, 0]] # orange, blue
pts_ball = deque(maxlen = 80)
trail_points = [deque(maxlen = 80), deque(maxlen = 80)]
	
cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 480)

while True:
	ret, frame = cap.read()

	if not ret:
		break

	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	ball_edges = findBall(hsv, ballMin, ballMax, pts_ball)

	# Draw balls trail
	for i in range(1, len(pts_ball)):
		if pts_ball[i - 1] is None or pts_ball[i] is None:
			continue
		trails_size = int(np.sqrt(80 / float(i + 1)) * 1.9)
		cv2.line(frame, pts_ball[i - 1], pts_ball[i], (0, 255, 255), trails_size)

	findColorAndLine(hsv, frame, markerColors)

	# Draw markers trail
	for idx, dq_pts in enumerate(trail_points): 
		for i in range(1, len(dq_pts)):
			if dq_pts[i - 1] is None or dq_pts[i] is None:
				continue
			trails_size = int(np.sqrt(80 / float(i + 1)) * 1.9)
			cv2.line(frame, dq_pts[i - 1], dq_pts[i], myColors[idx], trails_size)


	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()
