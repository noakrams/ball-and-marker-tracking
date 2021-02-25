# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

def findColor(hsv, frame, markerColors):
	color_count = 0
	for color in markerColors:
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
					trail_points[color_count].appendleft((int(x2) , int(y2)))
				else:
					trail_points[color_count].appendleft((int(x1), int(y1)))
		color_count += 1



# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--trail", type = int, default = 50, help="max trail size")
# ap.add_argument("-b", "--ball", help="detect ball")
# ap.add_argument("-m", "--marker", help="detect ball")
args = vars(ap.parse_args())
ballMin = np.array([22, 50, 50])
ballMax = np.array([50, 255, 255])
markerColors = [[0, 50, 250, 56, 255, 255],
				[50, 112, 134, 250, 255, 255]] #orange, blue
myColors = [[255, 255, 0], [0, 255, 255]] #orange, blue
orangeMin = np.array([0, 50, 250]) # 0 0 250
orangeMax = np.array([56, 255, 255])
pts_ball = deque(maxlen = args["trail"])
trail_points = [deque(maxlen = args["trail"]), deque(maxlen = args["trail"])]

	
cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 480)

# allow the camera or video file to warm up
time.sleep(2.0)


# keep looping
while True:
	# grab the current frame
	ret, frame = cap.read()

	if not ret:
		break

	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

	# Tennis ball ------------------------------------------------------------------------
	tennis_mask = cv2.inRange(hsv, ballMin, ballMax)
	tennis_mask = cv2.dilate(tennis_mask, None, iterations=2)
	tennis_mask = cv2.erode(tennis_mask, None, iterations=2)
	size = tennis_mask.shape

	# Marker line ------------------------------------------------------------------------
	# marker_mask = cv2.inRange(hsv, orangeMin, orangeMax)
	# marker_mask = cv2.dilate(marker_mask, None, iterations=2)
	# marker_mask = cv2.erode(marker_mask, None, iterations=2)
	# edges_line = cv2.Canny(marker_mask, 75, 150)

	# from internet --------------------------------------------------------------------------------

	# cnts = cv2.findContours(tennis_mask.copy(), cv2.RETR_EXTERNAL,
	# 	cv2.CHAIN_APPROX_SIMPLE)
	# cnts = imutils.grab_contours(cnts)
	# center = None

	# # only proceed if at least one contour was found

	# if len(cnts) > 0:
    		
	# 	# find the largest contour in the tennis_mask, then use
	# 	# it to compute the minimum enclosing circle and
	# 	# centroid

	# 	c = max(cnts, key=cv2.contourArea)
	# 	((x, y), radius) = cv2.minEnclosingCircle(c)
	# 	M = cv2.moments(c)
	# 	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

	# 	# only proceed if the radius meets a minimum size

	# 	if radius > 10:
    			
	# 		# draw the circle and centroid on the frame,
	# 		# then update the list of tracked points

	# 		cv2.circle(frame, (int(x), int(y)), int(radius),
	# 			(0, 255, 255), 2)
	# 		cv2.circle(frame, center, 5, (0, 0, 255), -1)

	# # update the points queue

	# pts.appendleft(center)

# hough circles with cv2 ---------------------------------------------------------------------------------------
	h, s = 0.0, 0.0
	ball_circles = cv2.HoughCircles(tennis_mask, cv2.HOUGH_GRADIENT, 1,
	80, param1=50, param2=10, minRadius=20, maxRadius=50)
	if ball_circles is not None:
		ball_circles = np.uint16(np.around(ball_circles))

		for circle in ball_circles[0, :]:
			for m in range(-10, 10):
				for n in range(-10, 10):
					if 0 <= (circle[1] + m) < size[0] and 0 <= (circle[0] + n) < size[1]:
						h += tennis_mask[circle[1]+m, circle[0]+n]
						s += 1
			tmp = h / s
			print(tmp)
			if h / s > 70 and circle[2] > 20:
				cv2.circle(frame, (int(circle[0]), int(circle[1])), int(circle[2]), (255, 0, 0), 2)
				center = (int(circle[0]), int(circle[1]))
				pts_ball.appendleft(center)
    	
	for i in range(1, len(pts_ball)):
		if pts_ball[i - 1] is None or pts_ball[i] is None:
			continue
		thickness = int(np.sqrt(args["trail"] / float(i + 1)) * 1.9)
		cv2.line(frame, pts_ball[i - 1], pts_ball[i], (255, 0, 255), thickness)

	findColor(hsv, frame, markerColors)
	
	for idx, dq_pts in enumerate(trail_points): 
		for i in range(1, len(dq_pts)):
			if dq_pts[i - 1] is None or dq_pts[i] is None:
				continue
			thickness = int(np.sqrt(args["trail"] / float(i + 1)) * 1.9)
			cv2.line(frame, dq_pts[i - 1], dq_pts[i], myColors[idx], thickness)


	# cv2.imshow("tennis_mask", tennis_mask)
	# cv2.imshow("marker_mask", marker_mask)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()