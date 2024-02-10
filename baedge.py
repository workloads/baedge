""" Baedge Library """

import os
import logging
import importlib
import qrcode

from PIL import Image, ImageDraw, ImageFont

# Baedge environment configuration
font_face = os.getenv("BAEDGE_FONT_FACE", "./fonts/RobotoMono/regular.ttf")
font_size = int(os.getenv("BAEDGE_FONT_SIZE", "15"))
screen_model = os.getenv("BAEDGE_SCREEN_MODEL", "2in9b")
screen_revision = os.getenv("BAEDGE_SCREEN_REVISION", "_v3")

# (human) wearer configuration
wearer_name = os.getenv("BAEDGE_WEARER_NAME", "{Ba,e}dge")
wearer_title = os.getenv("BAEDGE_WEARER_TITLE", "Orchestration at the Edge of Human and Compute.")
wearer_social = os.getenv("BAEDGE_WEARER_SOCIAL", "@wrklds")
wearer_link = os.getenv("BAEDGE_WEARER_LINK", "https://workloads.io")

# Nomad Environment configuration
nomad_alloc_id = os.getenv("NOMAD_SHORT_ALLOC_ID", "n/a")
nomad_addr_http = os.getenv("NOMAD_ADDR_http", "http://127.0.0.0")

log_level = os.getenv("LOG_LEVEL", "INFO")

# enable logging at the specified level
logging.basicConfig(level=log_level)

# screen layout configuration
ASSETS_DIR = '/opt/baedge-assets/'

coordinates = {
  # QR code is located in the bottom right corner
  "qrcode": '5, 5'
}

media = {
  # TODO: use PNG?
  "company_icon": ASSETS_DIR + 'hashicorp-icon-32.BMP'
}

# conditionally import the correct library depending on env vartiables describing the EPD size
epd_lib = importlib.import_module("lib.waveshare_epd.epd" + screen_model + screen_revision)
logging.debug("[config] load EPD Library for Model %s (Rev: %s)", screen_model, screen_revision)


def write_socials_info(epd):
    """ write socials info to eInk screen """
    text = wearer_name + "\n" + wearer_title + "\n" + wearer_social

    try:
        font = ImageFont.truetype(font_face, font_size)

        logging.debug("[write_socials] write to screen")
        # 255 = clear background frame
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)
        draw.text((coordinates["qrcode"]), text, font=font, fill=0)

        qr = qrcode.QRCode(version=1, box_size=4)
        qr.add_data(wearer_link)
        qr.make(fit=True)
        qri = qr.make_image()

        # TODO: use logging
        # should this say "writing QR image?"
        print(qri)
        image.paste(qri, (120, 60))

        epd.display(epd.getbuffer(image))

        logging.debug("[write_socials_info] sleep screen")
        # epd.sleep()

    except IOError as e:
        logging.error("[write_socials_info] exception occurred")
        logging.exception(e)


def write_baedge_info(epd):
    """ write Baedge info to eInk screen """
    logging.debug("[write_baedge_info] write to screen")

    # TODO: move this up and define more globally
    text = "{Ba,e}dge\n workloads.io/baedge "

    try:
        font = ImageFont.truetype(font_face, font_size)

        # 255 = clear background frame
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        draw.text((coordinates["qrcode"]), text, font=font, fill=0)

        epd.display(epd.getbuffer(image))
        logging.debug("[write_baedge_info] sleep screen")
        # epd.sleep()

    except IOError as e:
        logging.error("[write_baedge_info] exception occurred")
        logging.exception(e)


def write_nomad_info(epd):
    """ write Nomad info to eInk screen """
    logging.debug("[write_nomad_info] write to screen")

    try:
        font = ImageFont.truetype(font_face, font_size)
        text = nomad_alloc_id + "\n" + nomad_addr_http
        nimage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(nimage)

        # header, containing HashiCorp logo + white "Nomad" text on a black banner
        company_icon = Image.open(media["company_icon"])

        nimage.paste(company_icon, (0, 0))
        # draw a black rectangle on the top
        draw.rectangle((32, 0, 750, 31), fill=0)
        # write out Nomad in white
        draw.text((40, 0), "Nomad", font=font, fill=255)

        # write out Nomad info in black
        draw.text((0, 50), text, font=font, fill=0)

        # write to screen
        epd.display(epd.getbuffer(nimage))

        logging.debug("[write_nomad_info] sleep screen")
        # epd.sleep()

    except IOError as e:
        logging.error("[write_nomad_info] exception occurred")
        logging.exception(e)


def init_screen():
    """ initialize eInk screen """
    logging.debug("[init_screen]")

    try:
        epd = epd_lib.EPD()

        # TODO: remove or use
        font = ImageFont.truetype(font_face, font_size)

        logging.debug("[init_screen] init screen")
        epd.init()

        logging.debug("[init_screen] clear screen")
        epd.Clear()

        """
        # 255 = clear background frame
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)
        draw.text((coordinates["qrcode"]), text, font=font, fill=0)

        epd.display_Base(epd.getbuffer(image))
        epd.sleep()
        """
        return epd

    except IOError as e:
        logging.error("[init_screen] exception occurred")
        logging.exception(e)

        return None


def clear_screen(epd):
    """ clear content of eInk screen """
    logging.debug("[clear_screen]")

    try:
        epd.Clear()

        logging.debug("[clear_screen] sleep screen")
        epd.sleep()

    except IOError as e:
        logging.error("[clear_screen] exception occurred")
        logging.exception(e)


def write_text(epd, text, style):
    """ write textual content to eInk screen """
    logging.debug("[write_to_screen] text: %s", text)
    logging.debug("[write_to_screen] style: %s", style)

    # TODO: move this up and define more globally
    font = ImageFont.truetype(font_face, font_size)

    try:
        epd.init()
        # epd.Clear()

        image = Image.new('1', (epd.height, epd.width), 255)

        draw = ImageDraw.Draw(image)
        draw.text((5, 60), text, font=font, fill=0)

        epd.display(epd.getbuffer(image))

        """
        # attempt at partial refresh, TODO
        epd.display_Base_color(0xff)

        # 255 = clear background frame
        image = Image.new('1', (epd.height, epd.width), 0xff)  # `0xff` = `255`
        draw = ImageDraw.Draw(image)
        # the numbers are coordinates on which to draw
        draw.rectangle((10, 110, 120, 150), fill=255)
        draw.text((10, 110), text, font=font, fill=0)
        newimage = image.crop([10, 110, 120, 150])
        image.paste(newimage, (10, 110))
        epd.display_Partial(epd.getbuffer(image), 110, epd.height - 120, 150, epd.height - 10)
        """
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


"""
def write_to_screen(epd, text, image):
    #write content to eInk screen
    logging.debug("[write_to_screen] text: %s", text)
    logging.debug("[write_to_screen] image: %s", image)

    if not len(text) > 0 and not len(image) > 0:
        logging.error("[write_to_screen] `image` and `text` are empty, nothing to display")
        return False

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
