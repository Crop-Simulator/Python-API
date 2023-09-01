import cv2
import numpy as np


def on_trackbar(val):
    pass


def segment_plant_from_dirt_interactive(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    cv2.namedWindow('Segmented Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Segmented Image', 600, 600)

    # Trackbars for HSV thresholds
    cv2.createTrackbar('Lower H', 'Segmented Image', 43, 179, on_trackbar)
    cv2.createTrackbar('Lower S', 'Segmented Image', 18, 255, on_trackbar)
    cv2.createTrackbar('Lower V', 'Segmented Image', 102, 255, on_trackbar)
    cv2.createTrackbar('Upper H', 'Segmented Image', 105, 179, on_trackbar)
    cv2.createTrackbar('Upper S', 'Segmented Image', 255, 255, on_trackbar)
    cv2.createTrackbar('Upper V', 'Segmented Image', 255, 255, on_trackbar)

    # Trackbars for smoothing operations
    cv2.createTrackbar('Closing Size', 'Segmented Image', 7, 30, on_trackbar)
    cv2.createTrackbar('Blur Size', 'Segmented Image', 10, 30, on_trackbar)

    while True:
        lower_h = cv2.getTrackbarPos('Lower H', 'Segmented Image')
        lower_s = cv2.getTrackbarPos('Lower S', 'Segmented Image')
        lower_v = cv2.getTrackbarPos('Lower V', 'Segmented Image')
        upper_h = cv2.getTrackbarPos('Upper H', 'Segmented Image')
        upper_s = cv2.getTrackbarPos('Upper S', 'Segmented Image')
        upper_v = cv2.getTrackbarPos('Upper V', 'Segmented Image')

        closing_size = cv2.getTrackbarPos('Closing Size', 'Segmented Image')
        blur_size = cv2.getTrackbarPos('Blur Size', 'Segmented Image')

        lower_green = np.array([lower_h, lower_s, lower_v])
        upper_green = np.array([upper_h, upper_s, upper_v])

        mask_green = cv2.inRange(image_hsv, lower_green, upper_green)

        # Apply closing operation (dilation followed by erosion)
        kernel = np.ones((closing_size, closing_size), np.uint8)
        mask_closed = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)

        # Apply Gaussian blur
        if blur_size % 2 == 0:  # blur size needs to be odd
            blur_size += 1
        mask_blurred = cv2.GaussianBlur(mask_closed, (blur_size, blur_size), 0)

        cv2.imshow('Segmented Image', mask_blurred)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


segment_plant_from_dirt_interactive("../demo_data/test_extract/1_frame_0.jpg")
