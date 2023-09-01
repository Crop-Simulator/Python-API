import cv2
import numpy as np
from enum import Enum, auto


class ToolMode(Enum):
    ERASER = auto()
    BRUSH = auto()
    RECTANGLE = auto()


drawing = False  # true if mouse is pressed
tool_mode = ToolMode.ERASER
ix, iy = -1, -1
image_aspect_ratio = 1
mask_blurred = None


class TrackbarParameters:
    def __init__(self):
        self.display_width = None

        self.lower_h = None
        self.lower_s = None
        self.lower_v = None
        self.upper_h = None
        self.upper_s = None
        self.upper_v = None

        self.closing_size = None
        self.blur_size = None

        self.brush_size = None

    def callback_display_width(self, val):
        global image_aspect_ratio
        self.display_width = val
        cv2.resizeWindow("Images Display", val, int(val / image_aspect_ratio))

    def callback_lower_h(self, val):
        self.lower_h = val

    def callback_lower_s(self, val):
        self.lower_s = val

    def callback_lower_v(self, val):
        self.lower_v = val

    def callback_upper_h(self, val):
        self.upper_h = val

    def callback_upper_s(self, val):
        self.upper_s = val

    def callback_upper_v(self, val):
        self.upper_v = val

    def callback_closing_size(self, val):
        self.closing_size = val

    def callback_blur_size(self, val):
        self.blur_size = val

    def callback_brush_size(self, val):
        self.brush_size = val

trackbar_parameters = TrackbarParameters()


def on_trackbar(val):
    # This function is a dummy callback when trackbar values change.
    pass


# def callback_change_image_display_size(val):
#     global image_aspect_ratio
#     cv2.resizeWindow("Images Display", val, int(val / image_aspect_ratio))


# Mouse callback function
def callback_draw_mask(event, x, y, flags, param):
    global ix, iy, drawing, mask_blurred

    brush_size = cv2.getTrackbarPos('Brush Size', "Tools Window")

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if tool_mode is ToolMode.BRUSH:
                cv2.circle(mask_blurred, (x, y), brush_size, 255, -1)
                print(f"[Debug] {tool_mode} on ({x}, {y})")

            elif tool_mode is ToolMode.ERASER:
                cv2.circle(mask_blurred, (x, y), brush_size, 0, -1)
                print(f"[Debug] {tool_mode} on ({x}, {y})")

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if tool_mode is ToolMode.RECTANGLE:
            cv2.rectangle(mask_blurred, (ix, iy), (x, y), 255, -1)


def interactive_annotator(image_path):
    global mask_blurred, image_aspect_ratio, tool_mode, trackbar_parameters

    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    image_aspect_ratio = image.shape[1] / image.shape[0]

    # Convert the image from BGR to HSV (Hue, Saturation, Value)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Initial definition
    mask_blurred = np.zeros_like(image[:, :, 0])

    cv2.namedWindow("Tools Window", cv2.WINDOW_NORMAL)

    cv2.namedWindow("Images Display", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Images Display", callback_draw_mask)

    # Image window resize
    cv2.createTrackbar("Disp Width", "Tools Window", 800, 2000, trackbar_parameters.callback_display_width)
    target_window_width = cv2.getTrackbarPos("Disp Width", "Tools Window")
    cv2.resizeWindow("Images Display", target_window_width, int(target_window_width / image_aspect_ratio))

    # Trackbars for HSV thresholds
    cv2.createTrackbar('Lower H', "Tools Window", 35, 179, trackbar_parameters.callback_lower_h)
    cv2.createTrackbar('Lower S', "Tools Window", 40, 255, trackbar_parameters.callback_lower_s)
    cv2.createTrackbar('Lower V', "Tools Window", 40, 255, trackbar_parameters.callback_lower_v)
    cv2.createTrackbar('Upper H', "Tools Window", 85, 179, trackbar_parameters.callback_upper_h)
    cv2.createTrackbar('Upper S', "Tools Window", 255, 255, trackbar_parameters.callback_upper_s)
    cv2.createTrackbar('Upper V', "Tools Window", 255, 255, trackbar_parameters.callback_upper_v)

    # Trackbars for smoothing operations
    cv2.createTrackbar('Closing Sz', "Tools Window", 1, 30, trackbar_parameters.callback_closing_size)
    cv2.createTrackbar('Blur Size', "Tools Window", 1, 30, trackbar_parameters.callback_blur_size)

    # Trackbars for drawing tools
    cv2.createTrackbar('Brush Size', "Tools Window", 5, 50, trackbar_parameters.callback_brush_size)

    while True:
        # Define a mask for green color (which might represent plants)
        lower_green = np.array([trackbar_parameters.lower_h, trackbar_parameters.lower_s, trackbar_parameters.lower_v])
        upper_green = np.array([trackbar_parameters.upper_h, trackbar_parameters.upper_s, trackbar_parameters.upper_v])

        mask_green = cv2.inRange(image_hsv, lower_green, upper_green)

        # Apply closing operation (dilation followed by erosion)
        kernel = np.ones((trackbar_parameters.closing_size, trackbar_parameters.closing_size), np.uint8)
        mask_closed = cv2.morphologyEx(mask_green, cv2.MORPH_CLOSE, kernel)

        # Apply Gaussian blur
        if trackbar_parameters.blur_size % 2 == 0:  # blur size needs to be odd
            trackbar_parameters.blur_size += 1
        mask_blurred = cv2.GaussianBlur(mask_closed, (trackbar_parameters.blur_size, trackbar_parameters.blur_size), 0)

        # Display the segmented image
        cv2.imshow("Images Display", mask_blurred)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('b'):
            tool_mode = ToolMode.BRUSH
            print(f"[Debug] mode changed to {tool_mode}")
        elif key == ord('e'):
            tool_mode = ToolMode.ERASER
            print(f"[Debug] mode changed to {tool_mode}")
        elif key == ord('r'):
            tool_mode = ToolMode.RECTANGLE
            print(f"[Debug] mode changed to {tool_mode}")
        elif key == ord('q') or key == 27:
            # press "q" or "esc" to quit
            break

        # if window closed, break
        if cv2.getWindowProperty("Tools Window", cv2.WND_PROP_VISIBLE) < 1 or \
                cv2.getWindowProperty("Images Display", cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()


# Test the function
interactive_annotator("../demo_data/test_extract/1_frame_0.jpg")
