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
# This makes it cumbersome to develop on non-RPi devices, so we set `epd_library` to an empty object
if os.path.exists("/proc/cpuinfo"):
    # conditionally import the correct library depending on vartiables describing the EPD model and revision
    hardware_model = cfg.baedge["hardware"]["model"]
    hardware_revision = cfg.baedge["hardware"]["revision"]

    hlp.log_debug(__name__, 'load EPD Library for Model `' + hardware_model + '` (Rev: `' + hardware_revision + '`)')
    epd_library = importlib.import_module("lib.waveshare_epd.epd" + hardware_model + hardware_revision)

else:
    hlp.log_debug(__name__, 'skip load EPD Library on unsupported system')
    epd_library = {}

class EPD:
  def __init__(self):
    # Initialize your EPD object here
    pass


def initialize_screen():
    """
    Initialize screen for use

    Parameters:
        None

    Returns:
        object: Object containing EPD library and configuration
    """

    hlp.log_debug('initialize_screen', 'init')

    try:
        epd = epd_library.EPD()

        hlp.log_debug('initialize_screen', 'initialize screen')
        epd.init()

        hlp.log_debug('initialize_screen', 'clear screen')
        epd.Clear()

        hlp.log_debug('initialize_screen', 'end')
        return epd

    except IOError as e:
        hlp.log_exception('initialize_screen', e)
        return None


def clear_screen(epd, sleep_screen):
    """
    Clear contents on screen

    Parameters:
        epd (object):        Object containing EPD library and configuration
        sleep_screen (bool): Boolean indicating wether to sleep display or not

    Returns:
        bool: Boolean True if screen was cleared successfully
    """

    hlp.log_debug('clear_screen', 'init')

    try:
        hlp.log_debug('clear_screen', 'clear screen')
        epd.Clear()

        # only sleep if requested
        if sleep_screen:
            hlp.log_debug('clear_screen', 'sleep screen')
            epd.sleep()

        hlp.log_debug('clear_screen', 'end')
        return True

    except IOError as e:
        hlp.log_exception('clear_screen', e)
        return None


def write_screen(epd, screen, sleep_screen=False):
    """
    Write contents to screen

    Parameters:
        epd (object):        Object containing EPD library and configuration
        screen (string):     String indicating which screen to load data from
        sleep_screen (bool): Boolean indicating wether to sleep display or not

    Returns:
        bool: Boolean True if contents were written successfully
    """

    hlp.log_debug('write_screen', 'init')

    # load screen data from common object
    hlp.log_debug('write_screen', 'load screen data for `' + screen + '`')
    screen = cfg.screens[screen]
    hlp.log_debug('write_screen:screen', screen)

    try:
        # assemble font information
        # see https://pillow.readthedocs.io/en/latest/reference/ImageFont.html#PIL.ImageFont.truetype
        font = ImageFont.truetype(
            screen["font"]["face"],
            screen["font"]["size"],
        )

        # create canvas for downstream population with relevant data
        # see https://pillow.readthedocs.io/en/latest/reference/Image.html#PIL.Image.new
        canvas = Image.new(
            mode=cfg.baedge["image_mode"],
            size=(5, 5),  # (epd.height, epd.width),
            color=255,
        )

        # draw initial image to canvas
        draw = ImageDraw.Draw(canvas)

        # iterate over text items for screen
        for item in screen["texts"]:
            text_content = item["content"]
            text_coordinates = item["coordinates"]

            # assemble text object
            # see https://pillow.readthedocs.io/en/latest/reference/ImageDraw.html#PIL.ImageDraw.Draw
            draw.text(
                text_coordinates,
                text_content,
                font=font,
                fill=0
            )

        # check if QR Code configuration is present and prep QR code image
        if not screen["qrcode"]:
            hlp.log_debug('write_screen', 'skip QR code configuration')

        else:
            if screen["qrcode"]["content"] and screen["qrcode"]["coordinates"]:
                try:
                    qrc_content = screen["qrcode"]["content"]
                    qrc_coordinates = screen["qrcode"]["coordinates"]

                    hlp.log_debug('write_screen', 'prep QR code image')

                    # see https://pypi.org/project/qrcode/#advanced-usage
                    qrc_image = qrcode.QRCode(
                        box_size=cfg.baedge["qrcode"]["box_size"],
                        version=cfg.baedge["qrcode"]["version"],
                    )

                    # add data to image and make it fit the bounding box
                    qrc_image.add_data(qrc_content)
                    qrc_image.make(cfg.baedge["qrcode"]["fit"])

                    hlp.log_debug('write_screen:qrcode_image', qrc_image)
                    qrc_image.make_image()

                    hlp.log_debug('write_screen', 'place QR code image at coordinates: ' + str(qrc_coordinates))
                    # canvas.paste(qrc_image, qrc_coordinates)

                except ValueError as e:
                    hlp.log_exception('write_screen', e)
                    return None

        # get buffered canvas data and update display
        epd.display(epd.getbuffer(canvas))

        # only sleep if requested
        if sleep_screen:
            hlp.log_debug('write_screen', 'sleep screen')
            epd.sleep()

        hlp.log_debug('write_screen', 'end')
        return True

    except IOError as e:
        hlp.log_exception('write_screen', e)
        return False
