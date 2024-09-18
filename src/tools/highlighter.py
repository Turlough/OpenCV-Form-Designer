import cv2
from src.models.rectangle import Rectangle
from src.tools import common


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
        blurred = cv2.GaussianBlur(gray, (3, 3), 150)
        _, binary = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)
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
        b = common.little_crop_border
        base_scale = common.design_resolution / common.index_resolution
        scaled = cv2.resize(self.image, None, fx=base_scale, fy=base_scale)
        cropped = scaled[r.y1 - b:r.y2 + b, r.x1 - b:r.x2 + b]
        scale *= common.design_scale
        return cv2.resize(cropped, None, fx=scale, fy=scale)
        # return cropped

    def scaled_and_highlighted(self, scale: float = 1.0):
        blurred = cv2.GaussianBlur(self.image, (3, 3), 0)
        return cv2.resize(blurred, None, fx=scale, fy=scale)
