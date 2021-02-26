# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

def findColorAndLine(hsv, frame, markerColors):
	masks = []
	for idxColor, color in enumerate(markerColors):
		lower = np.array(color[0:3])
		upper = np.array(color[3:6])
		mask = cv2.inRange(hsv, lower, upper)
		masks.append(mask)
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
	return masks

# hough circles with cv2
def findBall(hsv, ballMin, ballMax, pts_ball):
	tennis_mask = cv2.inRange(hsv, ballMin, ballMax)
	tennis_mask = cv2.dilate(tennis_mask, None, iterations=2)
	tennis_mask = cv2.erode(tennis_mask, None, iterations=2)
	size = tennis_mask.shape
	h, s = 0.0, 0.0
	ball_circles = cv2.HoughCircles(tennis_mask, cv2.HOUGH_GRADIENT, 1,
	80, param1=50, param2=10, minRadius=50, maxRadius=80)
	if ball_circles is not None:
		ball_circles = np.uint16(np.around(ball_circles))
		for circle in ball_circles[0, :]:
			for m in range(-30, 30):
				for n in range(-30, 30):
					if 0 <= (circle[1] + m) < size[0] and 0 <= (circle[0] + n) < size[1]:
						h += tennis_mask[circle[1]+m, circle[0]+n]
						s += 1
			tmp = h / s
			print(tmp)
			if h / s > 254 and circle[2] > 50:
				cv2.circle(frame, (int(circle[0]), int(circle[1])), int(circle[2]), (255, 0, 0), 2)
				center = (int(circle[0]), int(circle[1]))
				pts_ball.appendleft(center)
	return tennis_mask




ap = argparse.ArgumentParser()
ap.add_argument("-t", "--trail", type = int, default = 50, help="max trail size")
args = vars(ap.parse_args())
ballMin = np.array([17, 15, 18])
ballMax = np.array([76, 255, 255])
markerColors = [[0, 80, 183, 27, 255, 248],  # 0, 138, 157, 250, 255, 255
				[50, 112, 134, 250, 255, 255]] #orange, blue
myColors = [[0, 165, 255], [255, 165, 0]] #orange, blue
pts_ball = deque(maxlen = args["trail"])
trail_points = [deque(maxlen = args["trail"]), deque(maxlen = args["trail"])]

	
cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 480)

# allow the camera or video file to warm up
time.sleep(2.0)

while True:
	ret, frame = cap.read()

	if not ret:
		break

	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	tennis_mask = findBall(hsv, ballMin, ballMax, pts_ball)

	# Draw tennis ball 	
	for i in range(1, len(pts_ball)):
		if pts_ball[i - 1] is None or pts_ball[i] is None:
			continue
		thickness = int(np.sqrt(args["trail"] / float(i + 1)) * 1.9)
		cv2.line(frame, pts_ball[i - 1], pts_ball[i], (0, 255, 255), thickness)

	masks = findColorAndLine(hsv, frame, markerColors)
	
	# Draw marker's trail
	for idx, dq_pts in enumerate(trail_points): 
		for i in range(1, len(dq_pts)):
			if dq_pts[i - 1] is None or dq_pts[i] is None:
				continue
			thickness = int(np.sqrt(args["trail"] / float(i + 1)) * 1.9)
			cv2.line(frame, dq_pts[i - 1], dq_pts[i], myColors[idx], thickness)

	if masks is not None:
			cv2.imshow("orange", masks[0])
			cv2.imshow("blue", masks[1])
    				
	cv2.imshow("tennis_mask", tennis_mask)
	# cv2.imshow("marker_mask", marker_mask)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()
