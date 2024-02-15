""" application """

import logging

from PIL import Image, ImageDraw, ImageFont

import helpers as hlp
import config as cfg

# to do: move to a more logical place
FONT_FACE = "RobotoMono/regular.ttf"
FONT_SIZE = 15

"""
def write_to_screen(epd, text, image):
    try:
        # init_screen()
        epd.Clear()
        font_config = ImageFont.truetype(font_face, font_size)
        # 255 = clear background frame
        image = Image.new('1', (epd.height, epd.width), 255)

        draw = ImageDraw.Draw(image)
        draw.text((5, 60), text, font=font_config, fill=0)

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
"""


def write_text(epd, text, style):
    # attempt at partial refresh, TODO
    # epd.display_Base_color(0xff)
    #
    # # 255 = clear background frame
    # image = Image.new('1', (epd.height, epd.width), 0xff)  # `0xff` = `255`
    # draw = ImageDraw.Draw(image)
    # # the numbers are coordinates on which to draw
    # draw.rectangle((10, 110, 120, 150), fill=255)
    # draw.text((10, 110), text, font=font, fill=0)
    # newimage = image.crop([10, 110, 120, 150])
    # image.paste(newimage, (10, 110))
    # epd.display_Partial(epd.getbuffer(image), 110, epd.height - 120, 150, epd.height - 10)

    epd.sleep()


def write_nomad_info(epd):
    nimage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(nimage)

    # header, containing HashiCorp logo + white "Nomad" text on a black banner
    company_icon = Image.open(cfg.media["company_icon"])

    nimage.paste(company_icon, (0, 0))

    # draw a black rectangle on the top
    draw.rectangle((32, 0, 750, 31), fill=0)
