import cv2
import numpy as np

drawing = False  # true if mouse is pressed
mode = 'brush'  # can be 'brush', 'erase', or 'rect'
ix, iy = -1, -1
image_aspect_ratio = 1


def on_trackbar(val):
    # This function is a dummy callback when trackbar values change.
    pass

def change_image_display_size(val):
    global image_aspect_ratio
    cv2.resizeWindow("Images Display", val, int(val/image_aspect_ratio))

# Mouse callback function
def draw_mask(event, x, y, flags, param):
    global ix, iy, drawing, mask_blurred

    brush_size = cv2.getTrackbarPos('Brush Size', "Tools Window")

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode == 'brush':
                cv2.circle(mask_blurred, (x, y), brush_size, 255, -1)
            elif mode == 'erase':
                cv2.circle(mask_blurred, (x, y), brush_size, 0, -1)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == 'rect':
            cv2.rectangle(mask_blurred, (ix, iy), (x, y), 255, -1)


def change_mode(val):
    global mode
    if val == 0:
        mode = 'brush'
    elif val == 1:
        mode = 'erase'
    else:
        mode = 'rect'


def segment_plant_from_dirt_interactive(image_path):
    global mask_blurred, image_aspect_ratio

    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image_aspect_ratio = image.shape[1]/image.shape[0]

    # Convert the image from BGR to HSV (Hue, Saturation, Value)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Initial definition
    mask_blurred = np.zeros_like(image[:, :, 0])

    cv2.namedWindow("Tools Window", cv2.WINDOW_NORMAL)

    cv2.namedWindow("Images Display", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Images Display", draw_mask)

    # Trackbars for HSV thresholds
    cv2.createTrackbar('Lower H', "Tools Window", 35, 179, on_trackbar)
    cv2.createTrackbar('Lower S', "Tools Window", 40, 255, on_trackbar)
    cv2.createTrackbar('Lower V', "Tools Window", 40, 255, on_trackbar)
    cv2.createTrackbar('Upper H', "Tools Window", 85, 179, on_trackbar)
    cv2.createTrackbar('Upper S', "Tools Window", 255, 255, on_trackbar)
    cv2.createTrackbar('Upper V', "Tools Window", 255, 255, on_trackbar)

    # Trackbars for smoothing operations
    cv2.createTrackbar('Closing Sz', "Tools Window", 1, 30, on_trackbar)
    cv2.createTrackbar('Blur Size', "Tools Window", 1, 30, on_trackbar)

    # Trackbars for drawing tools
    cv2.createTrackbar('Tool', "Tools Window", 0, 2, change_mode)
    cv2.createTrackbar('Brush Size', "Tools Window", 5, 50, lambda x: x)

    # Image window resize
    cv2.createTrackbar('Img Width', "Tools Window", 800, 2000, change_image_display_size)
    target_window_width = cv2.getTrackbarPos('Img Width', "Tools Window")
    cv2.resizeWindow("Images Display", target_window_width, int(target_window_width/image_aspect_ratio))

    while True:
        # Get the current trackbar positions
        lower_h = cv2.getTrackbarPos('Lower H', "Tools Window")
        lower_s = cv2.getTrackbarPos('Lower S', "Tools Window")
        lower_v = cv2.getTrackbarPos('Lower V', "Tools Window")

        upper_h = cv2.getTrackbarPos('Upper H', "Tools Window")
        upper_s = cv2.getTrackbarPos('Upper S', "Tools Window")
        upper_v = cv2.getTrackbarPos('Upper V', "Tools Window")

        closing_size = cv2.getTrackbarPos('Closing Sz', "Tools Window")
        blur_size = cv2.getTrackbarPos('Blur Size', "Tools Window")

        # Define a mask for green color (which might represent plants)
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

        # Display the segmented image
        cv2.imshow("Images Display", mask_blurred)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('b'):
            mode = 'brush'
        elif key == ord('e'):
            mode = 'erase'
        elif key == ord('r'):
            mode = 'rect'
        elif key == ord('q'):
            break

        # if window closed, break
        if cv2.getWindowProperty("Tools Window", cv2.WND_PROP_VISIBLE) < 1 or \
                cv2.getWindowProperty("Images Display", cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()

# Test the function
segment_plant_from_dirt_interactive("../demo_data/test_extract/1_frame_0.jpg")
