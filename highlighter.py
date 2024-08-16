from glob import glob

import cv2

scale = 0.3


def show(image):
    blurred = cv2.GaussianBlur(image, (3, 3), 150)
    scaled = cv2.resize(blurred, None, fx=scale, fy=scale)

    cv2.imshow('Detected Boxes', scaled)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def load(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 150)
    _, binary = cv2.threshold(blurred, 252, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 5: Filter contours by shape (rectangular)
    boxes = []
    contours = [c for c in contours if cv2.contourArea(c) > 900]
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the contour has 4 vertices (rectangle)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            # if 0.8 < aspect_ratio < 1.2:  # Aspect ratio close to 1 for square boxes
            boxes.append((x, y, w, h))
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return image


if __name__ == '__main__':
    folder = r'C:\_PV\forms'
    files = glob(folder + r'\**\*.tif', recursive=True)
    for f in files:
        img = load(f)
        show(img)
