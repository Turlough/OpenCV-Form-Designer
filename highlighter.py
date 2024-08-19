from glob import glob
import cv2

from models.tickbox import Box, TickBox, TickBoxGroup


class Highlighter:
    image = None
    image_path: str
    json_path: str
    tick_boxes: list[TickBox]
    tick_box_groups: list[TickBoxGroup]

    def __init__(self, path: str):
        self.image_path = path
        self.json_path = path.replace('.tif', '.json')
        self.image = cv2.imread(path)
        self.tick_boxes = list()
        self.tick_box_groups = list()

    def detect_boxes(self):

        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 150)
        _, binary = cv2.threshold(blurred, 252, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Remove very small boxes. These are just noise.
        contours = [c for c in contours if cv2.contourArea(c) > 900]
        for index, contour in enumerate(contours):
            # Approximate the contour to a polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Check if the contour has 4 vertices (rectangle)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(contour)
                box = Box().from_xywh(x, y, w, h)
                name = f'Box_{index:0>3d}'
                self.tick_boxes.append(TickBox(name, box))

    def scaled_and_highlighted(self, scale: float = 1.0):
        img = self.image.copy()
        for tbg in self.tick_box_groups:
            p1, p2 = tbg.rectangle.rectangle()
            cv2.rectangle(img, p1, p2, (0, 255, 0), 2)

        for tb in self.tick_boxes:
            p1, p2 = tb.box.rectangle()
            cv2.rectangle(img, p1, p2, (0, 0, 255), 2)
        return cv2.resize(img, None, fx=scale, fy=scale)

    def add_tickbox_group(self, group: TickBoxGroup):
        self.tick_box_groups.append(group)


def show_with_cv2(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    folder = r'C:\_PV\forms'
    files = glob(folder + r'\**\*.tif', recursive=True)
    for f in files:
        h = Highlighter(f)
        h.detect_boxes()
        scaled = h.scaled_and_highlighted(0.3)
        for tb in h.tick_boxes:
            print(tb.name, tb.box.rectangle())
        show_with_cv2(scaled)
