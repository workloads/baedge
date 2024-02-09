#!/usr/bin/python3

import sys
import os
import logging
import datetime
import importlib
from PIL import Image,ImageDraw,ImageFont
import time

libdir = "./e-Paper/RaspberryPi_JetsonNano/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

picdir = "./e-Paper/RaspberryPi_JetsonNano/python/pic"

logging.basicConfig(level=logging.DEBUG)

# conditionally import the correct library depending on env vartiables describing the EPD size
waveshare_epd_revision = os.getenv("WAVESHARE_EPD_REVISION", "2")
waveshare_epd_model = os.getenv("WAVESHARE_EPD_MODEL", "2in7")
epd_lib = importlib.import_module("waveshare_epd.epd"+waveshare_epd_model+"_V"+waveshare_epd_revision)

## TODO: Find a way to persist the epd config and not have to reset the screen on each request
def init_screen():
    try:
        if 'epd' not in globals():
            epd = epd_lib.EPD()
            logging.debug("Initialize screen")
            epd.init()
            epd.Clear()
    except IOError as e:
        logging.exception(e)

def clear():
    try:
        epd = epd_lib.EPD()
        logging.debug("Initialize screen")
        epd.init()
        epd.Clear()
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        epd.sleep()
    except IOError as e:
        logging.exception(e)

def write_text(text, style):
#    init_screen()
    # if font is specified, use that one, otherwise use the default
    # TODO: handle font sizes automatically based on text length
    if style:
        font = ImageFont.truetype(os.path.join(picdir, style), 14)
    else:
        font = ImageFont.truetype('./dejavu-fonts-ttf-2.37/ttf/DejaVuSansMono.ttf',15)
    try:
        epd = epd_lib.EPD()
        logging.debug("Initialize screen")
        epd.init()
        epd.Clear()
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        # the numbers are coordinates on which to draw
        draw.text((5, 30), text, font = font, fill = 0)
        #    draw.line((80,80, 50, 100), fill=0)
        epd.display_Base(epd.getbuffer(Himage))
        epd.sleep()
    except IOError as e:
        logging.exception(e)


def write_image(image):
    """
        logging.debug("Read image file: " + filename)
        Himage = Image.open(filename)
        logging.info("Display image file on screen")

        if waveshare_epd75_version == "2B":
            Limage_Other = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
            epd.display(epd.getbuffer(Himage), epd.getbuffer(Limage_Other))
        else:
            epd.display(epd.getbuffer(Himage))
        epd.sleep()
    """
    return False

def write_to_screen(text, image):
    if not (len(text) > 0) and not (len(image) > 0):
        logging.error("Both image and text are empty")
        return False
    try:
        epd = epd_lib.EPD()
        logging.debug("Initialize screen")
        epd.init()
        epd.Clear()

        # the last number is the font size
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
        fontDejaVuSansMono15 = ImageFont.truetype('./dejavu-fonts-ttf-2.37/ttf/DejaVuSansMono.ttf',15)
        """
        # Full screen refresh at 2 AM
        if datetime.datetime.now().minute == 0 and datetime.datetime.now().hour == 2:
            logging.debug("Clear screen")
            epd.Clear()

        filename = sys.argv[1]

        logging.debug("Read image file: " + filename)
        Himage = Image.open(filename)
        logging.info("Display image file on screen")

        if waveshare_epd75_version == "2B":
            Limage_Other = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
            epd.display(epd.getbuffer(Himage), epd.getbuffer(Limage_Other))
        else:
            epd.display(epd.getbuffer(Himage))
        epd.sleep()
        """
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        # the numbers are coordinates on which to draw
        draw.text((5, 30), text, font = font18, fill = 0)
        draw.text((5, 60), text, font = fontDejaVuSansMono15, fill = 0)
    #    draw.line((80,80, 50, 100), fill=0)
        epd.display_Base(epd.getbuffer(Himage))
        epd.sleep()
    except IOError as e:
        logging.exception(e)

    except KeyboardInterrupt:
        logging.debug("Keyboard Interrupt - Exit")
        epd_lib.epdconfig.module_exit()
        exit()
