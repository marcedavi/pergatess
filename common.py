import cv2
import numpy as np
import sys
import os

def process(image, padding = 0, perspective = 0, threshold = 0):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape

    pts1 = np.float32([[0 + perspective, 0], [width + perspective, 0], [0, height], [width, height]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    image = cv2.warpPerspective(
        image,
        M,
        (width, height),
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255),
    )

    _, thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    _, thresh_inv = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)
    
    points = cv2.findNonZero(thresh_inv)
    x, y, w, h = cv2.boundingRect(points)
    left = x - padding
    top = y - padding
    right = x + w + padding
    bottom = y + h + padding
    if left < 0: left = 0
    if top < 0: top = 0
    if right > width: right = width
    if bottom > height: bottom = height
    image = thresh[top : bottom, left : right]

    return image


def get_dependencies_path():
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, 'dependencies')
    else:
        base_path = os.path.join(os.path.dirname(__file__), 'dependencies')
    
    return base_path