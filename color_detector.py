import cv2
import numpy as np

def empty(a):
    pass

def main():
    camera = cv2.VideoCapture(0)
    filter_type = 'HSV'
    cv2.namedWindow('Trackbars', cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Hue Min", "Trackbars", 0, 255, empty)
    cv2.createTrackbar("Sat Min", "Trackbars", 0, 255, empty)
    cv2.createTrackbar("Val Min", "Trackbars", 0, 255, empty)
    cv2.createTrackbar("Hue Max", "Trackbars", 255, 255, empty)
    cv2.createTrackbar("Sat Max", "Trackbars", 255, 255, empty)
    cv2.createTrackbar("Val Max", "Trackbars", 255, 255, empty)

    while True:
        ret, image = camera.read()

        if not ret:
            break

        imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
        s_min = cv2.getTrackbarPos("Sat Min", "Trackbars")
        v_min = cv2.getTrackbarPos("Val Min", "Trackbars")
        h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
        s_max = cv2.getTrackbarPos("Sat Max", "Trackbars")
        v_max = cv2.getTrackbarPos("Val Max", "Trackbars")

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(imgHSV, lower, upper)

        cv2.imshow("Original", image)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF is ord('q'):
            break


if __name__ == '__main__':
    main()
    