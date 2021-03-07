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

#### Installation
- Install collections, numpy, cv2 and imutils libraries.
- Run python color_detection.py and pick the right values of the mask
- Change the values of the trail and mask in the right places as mantioned in track.py
- Run ./track.py and start drawing

---

## References
- [Circle Hough Transform](https://en.wikipedia.org/wiki/Circle_Hough_Transform#:~:text=The%20circle%20Hough%20Transform%20(CHT,maxima%20in%20an%20accumulator%20matrix.)
- [Line Detection with Hough](https://towardsdatascience.com/lines-detection-with-hough-transform-84020b3b1549)

---

## License

MIT License

Copyright (c) [2017] [James Q Quick]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[Back To The Top](#read-me-template)

---

## Author Info

- Twitter - [@jamesqquick](https://twitter.com/jamesqquick)
- Website - [James Q Quick](https://jamesqquick.com)

[Back To The Top](#read-me-template)
