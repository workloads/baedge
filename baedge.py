"""Baedge Library """

import sys
import os
import logging
import importlib

from PIL import Image, ImageDraw, ImageFont

# application configuration
LIB_DIR = "./e-Paper/python/lib"
MEDIA_DIR = "./e-Paper/python/pic"

# environment configuration
font_face = os.getenv("BAEDGE_FONT_FACE", "./fonts/RobotoMono/Regular.ttf")
font_size = os.getenv("BAEDGE_FONT_SIZE", "15")
screen_model = os.getenv("BAEDGE_SCREEN_MODEL", "2in7")
screen_revision = os.getenv("BAEDGE_SCREEN_REVISION", "2")
log_level = os.getenv("LOG_LEVEL", "INFO")

# enable logging at the specified level
logging.basicConfig(level=log_level)

if os.path.exists(LIB_DIR):
    sys.path.append(LIB_DIR)

# conditionally import the correct library depending on env vartiables describing the EPD size
epd_lib = importlib.import_module("waveshare_epd.epd" + screen_model + "_V" + screen_revision)
logging.debug("[config] load EPD Library for Model %s (Rev: %s)",screen_model, screen_revision)

# initialize the eInk screen
epd = epd_lib.EPD()


## TODO: Find a way to persist the epd config and not have to reset the screen on each request
def init_screen():
    """ initialize eInk screen """
    try:
        if 'epd' not in globals():
            logging.debug("[init_screen] init screen")
            epd.init()

            logging.debug("[init_screen] clear screen")
            epd.Clear()

    except IOError as e:
        logging.error("[init_screen] exception occurred")
        logging.exception(e)


def clear_screen():
    """ clear content of eInk screen """
    logging.debug("[clear_screen]")

    try:
        init_screen()

        logging.debug("[clear_screen] sleep screen")
        epd.sleep()

    except IOError as e:
        logging.error("[clear_screen] exception occurred")
        logging.exception(e)


def write_text(text, style):
    """ write textual content to eInk screen """
    logging.debug("[write_to_screen] text: %s", text)
    logging.debug("[write_to_screen] style: %s", style)

#    init_screen()
    # if font is specified, use that one, otherwise use the default
    if style:
        font = ImageFont.truetype(os.path.join(MEDIA_DIR, style), 14)
    else:
        font = ImageFont.truetype(font_face, font_size)

    try:
        init_screen()

        # `255` clears the eInk screen
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        # the numbers are coordinates on which to draw
        draw.text((5, 30), text, font = font, fill = 0)
        #    draw.line((80,80, 50, 100), fill=0)
        epd.display_Base(epd.getbuffer(Himage))
        epd.sleep()

    except IOError as e:
        logging.error("[write_text] exception occurred")
        logging.exception(e)


def write_image(image):
    """ write image content to eInk screen """
    logging.debug("[write_image] image: %s", image)

    # TODO: implement image writing

    return False


def write_to_screen(text, image):
    """ write content to eInk screen """

    logging.debug("[write_to_screen] text: %s", text)
    logging.debug("[write_to_screen] image: %s", image)

    if not len(text) > 0 and not len(image) > 0:
        logging.error("[write_to_screen] `image` and `text` are empty, nothing to display")
        return False

    try:
        logging.debug("[write_to_screen] initialize screen")

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
        init_screen()

        font_config = ImageFont.truetype(font_face, font_size)

        # 255: clear the frame
        image = Image.new('1', (epd.height, epd.width), 255)

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
        epd.display_Base(epd.getbuffer(image))

        logging.debug("[write_text] sleep screen")
        epd.sleep()

    except IOError as e:
        logging.error("[write_text] exception occurred")
        logging.exception(e)

    except KeyboardInterrupt:
        logging.debug("[write_to_screen] keyboard interrupt")

        epd_lib.epdconfig.module_exit()
        sys.exit()
