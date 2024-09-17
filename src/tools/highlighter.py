from glob import glob
import cv2
import numpy as np

from src.models.rectangle import Rectangle


class Highlighter:
    image = None
    image_path: str
    boxes = list()
    tick_box_groups = list()

    @classmethod
    def from_path(cls, path):
        cls.image = cv2.imread(path)
        return cls()

    @classmethod
    def from_np_array(cls, image):
        cls.image = image
        return cls()

    def detect_boxes(self):

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (1, 1), 5)
        _, binary = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Remove very small boxes. These are just noise.
        contours = [c for c in contours if cv2.contourArea(c) > 900]
        rectangles: list[Rectangle] = list()
        for index, contour in enumerate(contours):
            # Approximate the contour to a polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Check if the contour has 4 vertices (coordinates)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(contour)
                rect = Rectangle().from_xywh(x, y, w, h)
                rectangles.append(rect)
        rectangles.sort(key=lambda r: r.y1)
        return rectangles

    def crop(self, r: Rectangle, scale: float):
        b = 50  # border
        cropped = self.image[r.y1 - b:r.y2 + b, r.x1 - b:r.x2 + b]
        return cv2.resize(cropped, None, fx=scale, fy=scale)

    def scaled_and_highlighted(self, scale: float = 1.0):
        blurred = cv2.GaussianBlur(self.image, (3, 3), 0)
        return cv2.resize(blurred, None, fx=scale, fy=scale)

    def scaled_and_translated(self, scale, x, y):
        """
        Scales the image by 'scale' factor and translates it by 'x' and 'y' pixels.
        Positive 'x' pads the left, negative 'x' crops from the left.
        Positive 'y' pads the top, negative 'y' crops from the top.

        :param x: Translation along the x-axis.
        :param y: Translation along the y-axis.
        :param scale: Scaling factor.
        """
        # Scale the image
        scaled_image = cv2.resize(self.image, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        height, width = scaled_image.shape[:2]
        crop_top = 0
        crop_left = 0
        top_pad = 0
        left_pad = 0

        # Handle vertical translation (y-axis)
        if y > 0:
            top_pad = int(y)
        elif y < 0:
            crop_top = min(int(abs(y)), height)

        # Handle horizontal translation (x-axis)
        if x > 0:
            left_pad = int(x)
        elif x < 0:
            crop_left = min(int(abs(x)), width)

        if crop_top > 0 or crop_left > 0:
            cropped_image = scaled_image[crop_top:height, crop_left:width]
        else:
            cropped_image = scaled_image

        # Pad the image if needed
        if top_pad > 0 or left_pad > 0:
            # Pad the image with zeros (black color)
            padded_image = cv2.copyMakeBorder(
                    cropped_image,
                    top=top_pad,
                    bottom=0,
                    left=left_pad,
                    right=0,
                    borderType=cv2.BORDER_CONSTANT,
                    value=[0, 0, 0]  # Black color padding
            )
        else:
            padded_image = cropped_image

        return padded_image
