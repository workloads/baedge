"""Baedge Library """

import sys
import os
import logging
import importlib
from PIL import Image,ImageDraw,ImageFont

from PIL import Image, ImageDraw, ImageFont

# application configuration
LIB_DIR = "./e-Paper/python/lib"
MEDIA_DIR = "./e-Paper/python/pic"

log_level = os.getenv("LOG_LEVEL", "INFO")

# enable logging at the specified level
logging.basicConfig(level=log_level)

if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

# environment configuration
font_face = os.getenv("BAEDGE_FONT_FACE", "./dejavu-fonts-ttf-2.37/ttf/DejaVuSansMono.ttf")
font_size = os.getenv("BAEDGE_FONT_SIZE", "15")
screen_model = os.getenv("BAEDGE_SCREEN_MODEL", "2in7")
screen_revision = os.getenv("BAEDGE_SCREEN_REVISION", "2")

# conditionally import the correct library depending on env vartiables describing the EPD size
epd_lib = importlib.import_module("waveshare_epd.epd" + screen_model + "_V" + screen_revision)
logging.debug("[config] load EPD Library for Model %s (Rev: %s)",screen_model, screen_revision)


## TODO: Find a way to persist the epd config and not have to reset the screen on each request
def init_screen():
    """ initialize eInk screen """
    try:
        if 'epd' not in globals():
            epd = epd_lib.EPD()
            logging.debug("Initialize screen")

            epd = epd_lib.EPD()
            epd.init()
            epd.Clear()
    except IOError as e:
        logging.debug("[init_screen] exception occurred")
        logging.exception(e)


def clear_screen():
    """ clear content of eInk screen """
    logging.debug("[clear_screen]")

    try:
        logging.debug("[clear_screen] initialize and clear screen")

        epd = epd_lib.EPD()

        epd.init()
        epd.Clear()

        # `255` clears the eInk screen
        Himage = Image.new('1', (epd.height, epd.width), 255)

        logging.debug("[clear] sleep screen")
        epd.sleep()

    except IOError as e:
        logging.debug("[clear_screen] exception occurred")
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

        logging.debug("[write_text] sleep screen")
        epd.sleep()

    except IOError as e:
        logging.debug("[write_text] exception occurred")
        logging.exception(e)

    except KeyboardInterrupt:
        logging.debug("[write_to_screen] keyboard interrupt")

        epd_lib.epdconfig.module_exit()
        sys.exit()
