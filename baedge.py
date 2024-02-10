""" Baedge Library """

import sys
import os
import logging
import importlib

from PIL import Image, ImageDraw, ImageFont

# application configuration
LIB_DIR = "./lib"

# environment configuration
font_face = os.getenv("BAEDGE_FONT_FACE", "./fonts/RobotoMono/regular.ttf")
font_size = int(os.getenv("BAEDGE_FONT_SIZE", "15"))
screen_model = os.getenv("BAEDGE_SCREEN_MODEL", "2in7")
screen_revision = os.getenv("BAEDGE_SCREEN_REVISION", "_V2")
log_level = os.getenv("LOG_LEVEL", "INFO")

# enable logging at the specified level
logging.basicConfig(level=log_level)


# conditionally import the correct library depending on env vartiables describing the EPD size
epd_lib = importlib.import_module("lib.waveshare_epd.epd" + screen_model + screen_revision)
logging.debug("[config] load EPD Library for Model %s (Rev: %s)",screen_model, screen_revision)

## TODO: Find a way to persist the epd config and not have to reset the screen on each request
def init_screen():
    """ initialize eInk screen """
    text = "{Ba,e}dge"
    try:
        epd = epd_lib.EPD()
        font = ImageFont.truetype(font_face, font_size)

        logging.debug("[init_screen] init screen")
        epd.init()

        logging.debug("[init_screen] clear screen")
        epd.Clear()

        # 255 = clear background frame
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)
        # the numbers are coordinates on which to draw
        draw.text((5, 5), text, font = font, fill = 0)

        epd.display_Base(epd.getbuffer(image))
        epd.sleep()

        return epd

    except IOError as e:
        logging.error("[init_screen] exception occurred")
        logging.exception(e)

        return None


def clear_screen(epd):
    """ clear content of eInk screen """
    logging.debug("[clear_screen]")

    try:
#        init_screen()

        logging.debug("[clear_screen] sleep screen")
        epd.sleep()

    except IOError as e:
        logging.error("[clear_screen] exception occurred")
        logging.exception(e)


def write_text(epd, text, style):
    """ write textual content to eInk screen """
    logging.debug("[write_to_screen] text: %s", text)
    logging.debug("[write_to_screen] style: %s", style)

    font = ImageFont.truetype(font_face, font_size)

    try:
        epd.init()
#        epd.Clear()

        # attempt
        epd.display_Base_color(0xff)


        # 255 = clear background frame
        image = Image.new('1', (epd.height, epd.width), 0xff)#255)
        draw = ImageDraw.Draw(image)
        # the numbers are coordinates on which to draw
        draw.rectangle((10, 110, 120, 150), fill = 255)
        draw.text((10, 110), text, font = font, fill = 0)
        newimage = image.crop([10, 110, 120, 150])
        image.paste(newimage, (10,110))
        epd.display_Partial(epd.getbuffer(image), 110, epd.height - 120, 150, epd.height - 10)

        #old full display write
        #epd.display(epd.getbuffer(image))
        epd.sleep()

    except IOError as e:
        logging.error("[write_text] exception occurred")
        logging.exception(e)


def write_image(epd, image):
    """ write image content to eInk screen """
    logging.debug("[write_image] image: %s", image)

    # this is a placeholder for the image writing functionality
    logging.debug(epd)

    # TODO: implement image writing

    return False


def write_to_screen(epd, text, image):
    """ write content to eInk screen """
    logging.debug("[write_to_screen] text: %s", text)
    logging.debug("[write_to_screen] image: %s", image)

    if not len(text) > 0 and not len(image) > 0:
        logging.error("[write_to_screen] `image` and `text` are empty, nothing to display")
        return False

    try:
#        init_screen()
        epd.Clear()
        font_config = ImageFont.truetype(font_face, font_size)
        # 255 = clear background frame
        image = Image.new('1', (epd.height, epd.width), 255)

        draw = ImageDraw.Draw(image)
        draw.text((5, 60), text, font = font_config, fill = 0)

        epd.display_Base(epd.getbuffer(image))

        logging.debug("[write_text] sleep screen")
        epd.sleep()

        return True

    except IOError as e:
        logging.error("[write_text] exception occurred")
        logging.exception(e)

        return False

    except KeyboardInterrupt:
        logging.debug("[write_to_screen] keyboard interrupt")

        epd.module_exit()
        sys.exit()
