""" application """

import importlib
import logging
import os
import platform
import qrcode

from PIL import Image, ImageDraw, ImageFont

import helpers as hlp
import config as cfg

# enable logging at the specified level
logging.basicConfig(level=cfg.app["logging"]["level"])

hlp.log_debug(__name__, 'detected platform: `' + platform.system() + '`')

# Waveshare's EPD library queries the content of `/proc/cpuinfo` for system information for string `Raspberry`
# This makes it cumbersome to develop on non-RPi devices, so we override `epd_library` and skip initialization
if os.path.exists("/proc/cpuinfo"):
    # conditionally import the correct library depending on vartiables describing the EPD model and revision
    hardware_model = cfg.baedge["hardware"]["model"]
    hardware_revision = cfg.baedge["hardware"]["revision"]

    hlp.log_debug(__name__, 'load EPD Library for Model `' + hardware_model + '` (Rev: `' + hardware_revision + '`)')
    epd_library = importlib.import_module("lib.waveshare_epd.epd" + hardware_model + hardware_revision)

    SKIP_INITIALIZE_SCREEN = False

else:
    hlp.log_info(__name__, 'skip load of EPD Library on unsupported system')
    epd_library = {}

    # set flag to skip initialization of screen on unsupported system
    SKIP_INITIALIZE_SCREEN = True


def initialize_screen():
    """
    Initialize screen for use

    Parameters:
        n/a

    Returns:
        object: Object containing EPD library and configuration
    """

    hlp.log_debug('initialize_screen', 'init function')

    try:
        epd = epd_library.EPD()

        hlp.log_debug('initialize_screen', 'initialize screen')
        epd.init()

        hlp.log_debug('initialize_screen', 'clear screen')
        epd.Clear()

        hlp.log_debug('initialize_screen', 'end function')
        return epd

    except IOError as e:
        hlp.log_exception('initialize_screen', e)
        return None


def clear_screen(epd, sleep_screen=False):
    """
    Clear contents on screen

    Parameters:
        epd (object):        Object containing EPD library and configuration
        sleep_screen (bool): Boolean indicating wether to sleep display or not

    Returns:
        bool: Boolean True if screen was cleared successfully
    """

    hlp.log_debug('clear_screen', 'init function')

    try:
        hlp.log_debug('clear_screen', 'clear screen')
        epd.Clear()

        # only sleep if requested
        if sleep_screen:
            hlp.log_debug('clear_screen', 'sleep screen')
            epd.sleep()

        hlp.log_debug('clear_screen', 'end function')
        return True

    except IOError as e:
        hlp.log_exception('clear_screen', e)
        return None


def write_screen(epd, screen_name, sleep_screen=False):
    """
    Write contents to screen

    Parameters:
        epd (object):         Object containing EPD library and configuration
        screen_name (string): String indicating which screen to load data from
        sleep_screen (bool):  Boolean indicating wether to sleep display or not

    Returns:
        bool: Boolean True if contents were written successfully
    """

    hlp.log_debug('write_screen', 'init function')

    # load screen data from common object
    hlp.log_debug('write_screen', 'load screen data for `' + screen_name + '`')
    screen = cfg.screens[screen_name]
    hlp.log_debug('write_screen:screen', screen_name)

    try:
        # assemble font information
        # see https://pillow.readthedocs.io/en/latest/reference/ImageFont.html#PIL.ImageFont.truetype
        font = ImageFont.truetype(
            screen["font"]["face"],
            screen["font"]["size"],
        )

        # create canvas for downstream population with relevant data
        # see https://pillow.readthedocs.io/en/latesmt/reference/Image.html#PIL.Image.new
        canvas = Image.new(
            mode=cfg.baedge["image_mode"],
            size=(epd.height, epd.width),
            color=255,
        )

        # draw initial image to canvas
        draw = ImageDraw.Draw(canvas)

        # iterate over image items for screen
        if "images" in screen:
            for item in screen["images"]:
                hlp.log_debug('write_screen:image', item)

                if item["content"] and item["coordinates"]:
                    content = item["content"]
                    coordinates = item["coordinates"]

                    hlp.log_debug('write_screen:image', 'write image')
                    # TODO: write image

                else:
                    hlp.log_debug('write_screen:image', 'incomplete data, skip write image')

        # iterate over shape items for screen
        if "shapes" in screen:
            for item in screen["shapes"]:
                hlp.log_debug('write_screen:shape', item)

                if item["coordinates"] and item["fill"] and item["type"]:
                    coordinates = item["coordinates"]
                    fill = item["fill"]
                    type = item["type"]

                    hlp.log_debug('write_screen:shape', 'write shape')
                    # TODO: write shape

                else:
                    hlp.log_debug('write_screen:shape', 'incomplete data, skip write shape')

        # iterate over text items for screen
        if "texts" in screen:
            for item in screen["texts"]:
                hlp.log_debug('write_screen:text', item)

                if "content" in item and "coordinates" in item and "fill" in item:
                    font_size = screen["font"]["size"]
                    # while the longest single line of text (based on splitting by \n, getting the longest one, and comparing its length)
                    while font.getlength(max(item["content"].split("\n"), key=len)) > max(epd.width, epd.height):
                        hlp.log_debug("write_scree:text", "Overriding font size to fit on screen")
                        font_size -= 1
                        font = ImageFont.truetype(
                            screen["font"]["face"],
                            font_size,
                        )

                    hlp.log_debug("write_screen:text", "Final font size, adjusted for tthe screen size:" + str(font_size))
                    content = item["content"]
                    coordinates = item["coordinates"]
                    fill = item["fill"]

                    hlp.log_debug('write_screen:text', 'write text')

                    # assemble text object
                    # see https://pillow.readthedocs.io/en/latest/reference/ImageDraw.html#PIL.ImageDraw.Draw
                    draw.text(
                        coordinates,
                        content.lstrip(),
                        font=font,
                        fill=fill
                    )
                    print(coordinates, content, font, fill)
                else:
                    hlp.log_debug('write_screen:text', 'incomplete data, skip write text')

        # check if QR Code configuration is present and prep QR code image
        if "qrcode" not in screen:
            hlp.log_debug('write_screen:qrcode', 'incomplete data, skip write QR code')

        else:
            if screen["qrcode"]["content"] and screen["qrcode"]["offset"]:
                try:
                    content = screen["qrcode"]["content"]

                    hlp.log_debug('write_screen:qrcode', 'prep QR code image')
                    # see https://pypi.org/project/qrcode/#advanced-usage
                    qrc_image = qrcode.QRCode(
                        box_size=cfg.baedge["qrcode"]["box_size"],
                        version=cfg.baedge["qrcode"]["version"],
                    )

                    # add data to image and make it fit the bounding box
                    qrc_image.add_data(content)
                    qrc_image.make(cfg.baedge["qrcode"]["fit"])

                    hlp.log_debug('write_screen:qrcode', qrc_image)
                    qrc_canvas = qrc_image.make_image()
                    print(qrc_canvas)
                    print(qrc_canvas.size)

                    coordinates = hlp.generate_relative_coordinates(
                        epd.height,
                        epd.width,
                        screen["qrcode"]["offset"],
                        qrc_canvas.size
                    )

                    hlp.log_debug('write_screen:qrcode', 'place QR code image at coordinates: ' + str(coordinates))
                    canvas.paste(qrc_canvas, coordinates)

                except ValueError as e:
                    hlp.log_exception('write_screen:qrcode', e)
                    return None

        print(canvas.show())
        print(canvas)

        # get buffered canvas data and update display
        epd.display(epd.getbuffer(canvas))

        # only sleep if requested
        if sleep_screen:
            hlp.log_debug('write_screen', 'sleep screen')
            epd.sleep()

        hlp.log_debug('write_screen', 'end function')
        return True

    except IOError as e:
        hlp.log_exception('write_screen', e)
        return False
