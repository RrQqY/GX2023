import math

import cv2


class CircleDetector(object):

    '''
	Parameters
	----------
	img: ndarray
		A color image.
	threshold: int or float
        Image binary threshold.
	minRadius: int or float
		Minimum value of circle radius.
	maxRadius: int or flaot
		Maximum value of circle radius.

	Returns
	-------
	A tuple of (center(x, y), size(w, h), angle)
	'''
    def detectCircles(self, image, threshold, minRadius, maxRadius):
        circles = list()
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        ret, thresh = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5), (-1, -1))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, (-1, -1))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, (-1, -1))

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if len(cnt) < 5:
                continue

            area = cv2.contourArea(cnt)
            if area < (minRadius**2) * math.pi or area > (maxRadius**2) * math.pi:
                continue

            arc_length = cv2.arcLength(cnt, True)
            radius = arc_length / (2 * math.pi)

            if not (minRadius < radius and radius < maxRadius):
                continue

            ellipse = cv2.fitEllipse(cnt)
            ratio = float(ellipse[1][0]) / float(ellipse[1][1])

            if ratio > 0.9 and ratio < 1.1:
                corner = cv2.approxPolyDP(cnt, 0.02 * arc_length, True)
                cornerNum = len(corner)
                if cornerNum > 4: # 当cornerNum=4时，识别矩形；而cornerNum>4时，识别圆
                    circles.append(ellipse)

        return circles
