# Marker and Ball tracking

![Project Image](Resources/messingAround.gif)



> Live Webcam Drawing

---

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [References](#references)
- [License](#license)
- [Author Info](#author-info)

---

### Description

I had two main goals when starting the project. The first is that I wanted to expand my knowledge in Hough Transform (circles and lines detection). The second is that I wanted to do a project related to painting because I really like to paint. For these reasons, I chose to use Hough Transform methods to detect a tennis ball and a marker in real-time. In this project I implemented a code that does the following:

1. Using a web camera, it can detect if there is a tennis ball or marker in the video frame. If a marker is detected, the color of the marker is detected as well (orange, blue or purple).
2. Track the ball or the marker as it moves inside the frame and draw the trail of the ball/marker.


#### Technologies

- OpenCV
- Python 2.7.17

[Back To The Top](#read-me-template)

---

## How To Use

- Install collections, numpy, cv2 and imutils libraries.
- Run python color_detection.py and pick the right values of the mask
- Change the values of the trail and mask in the right places as mantioned in track.py
- Run ./track.py and start drawing

---

## References
- [Circle Hough Transform](https://en.wikipedia.org/wiki/Circle_Hough_Transform#:~:text=The%20circle%20Hough%20Transform%20(CHT,maxima%20in%20an%20accumulator%20matrix.)
- [Line Detection with Hough](https://towardsdatascience.com/lines-detection-with-hough-transform-84020b3b1549)

---



## Author Info

- LinkedIn - [Noa Krams](https://www.linkedin.com/in/noa-krams/)

[Back To The Top](#Marker-and-Ball-tracking)
