from logging import debug, info
from pyautogui import screenshot, locate, locateOnScreen, locateCenterOnScreen
from numpy import array, ndarray, pi
from cv2 import cvtColor, COLOR_BGR2HSV, inRange, Canny, HoughLinesP
from PIL import ImageGrab

from src.helper import mouse_helper


def get_pixel_color_at_cursor():
    """Get the color of per cursor selected pixel"""
    x, y = mouse_helper.position()
    r, g, b = screenshot().getpixel((x, y))

    return x, y, r, g, b


def get_image_at_cursor(name="default", path="..\\assets\\skills\\", ix=25, iy=25):
    """Get the image of per cursor selected pixel"""
    x, y = mouse_helper.position()
    img = screenshot(region=(x, y, ix, iy))
    img.save(path + name + ".png")

    return x, y


def pixel_matches_color(x, y, exR, exG, exB, tolerance=25):
    """Get rgb color at coordinate"""
    r, g, b = screenshot().getpixel((x, y))

    if (
        (abs(r - exR) <= tolerance)
        and (abs(g - exG) <= tolerance)
        and (abs(b - exB) <= tolerance)
    ):
        return True
    return False


def line_detection(line_type="path"):
    """Recognition of a line by given color on the screen"""
    if line_type == "path":
        array_min = array([75, 120, 95])  # rgb color
        array_max = array([125, 250, 145])
        screen_box = (1650, 50, 1850, 250)  # region of the screen x, y, w, h
    elif line_type == "mob":
        array_min = array([95, 235, 105])
        array_max = array([185, 255, 135])
        screen_box = (400, 50, 1500, 870)

    image_grab = ImageGrab.grab(bbox=screen_box)
    np_array = array(image_grab)
    hsv = cvtColor(np_array, COLOR_BGR2HSV)
    mask = inRange(hsv, array_min, array_max)
    edges = Canny(mask, 50, 150, apertureSize=3, L2gradient=True)
    lines = HoughLinesP(
        image=edges,
        rho=1,
        theta=pi / 180,
        threshold=15,
        lines=array([]),
        minLineLength=5,
        maxLineGap=0,
    )

    if type(lines) is ndarray:
        for points in lines:
            x, y, w, h = points[0]
            info("found line type " + line_type + " at " + str(x) + ", " + str(y))
            return x, y
    return False


def locate_needle(
    needle,
    haystack=0,
    conf=0.8,
    loctype="l",
    grayscale=True,
    region=(715, 1005, 1205, 1060),
):
    """Searches the haystack image for the needle image, returning a tuple
    of the needle's coordinates within the haystack. If a haystack image is
    not provided, searches the client window or the overview window,
    as specified by the loctype parameter."""

    # with haystack image, return coordinates
    if haystack != 0:
        locate_var = locate(needle, haystack, confidence=conf, grayscale=grayscale)
        if locate_var is not None:
            debug(
                "found needle "
                + (str(needle))
                + " in haystack"
                + (str(haystack))
                + ", "
                + (str(locate_var))
            )
            return locate_var
        else:
            debug(
                "cant find needle "
                + (str(needle))
                + " in haystack"
                + (str(haystack))
                + ", "
                + (str(locate_var))
                + ", conf="
                + (str(conf))
            )
            return -1, -1

    # without haystack image, return 1 or 0
    elif loctype == "l":  # 'l' for regular 'locate'
        locate_var = locateOnScreen(
            needle, confidence=conf, region=region, grayscale=grayscale
        )
        if locate_var is not None:
            debug("found l image " + (str(needle)) + ", " + (str(locate_var)))
            # If the center of the image is not needed, don't return any coordinates.
            return True
        elif locate_var is None:
            debug("cannot find l image " + (str(needle)) + " conf=" + (str(conf)))
            return False

    # without haystack image, return coordinates
    elif loctype == "c":  # 'c' for 'center'
        locate_var = locateCenterOnScreen(
            needle, confidence=conf, region=region, grayscale=grayscale
        )
        if locate_var is not None:
            debug("found c image " + (str(needle)) + ", " + (str(locate_var)))
            # Return the xy coordinates for the center of the image, relative to the coordinate plane of the haystack.
            return locate_var
        elif locate_var is None:
            debug("cannot find c image " + (str(needle)) + ", conf=" + (str(conf)))
            return -1, -1
