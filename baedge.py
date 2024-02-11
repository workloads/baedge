""" application """

import logging
import importlib
import qrcode

from PIL import Image, ImageDraw, ImageFont

import helpers as hlp
import config as cfg

# enable logging at the specified level
logging.basicConfig(level=cfg.app["log_level"])

# TODO: move to a more logical place
FONT_FACE = cfg.baedge["fonts"]["path"] + "RobotoMono/regular.ttf"
FONT_SIZE = 15

# conditionally import the correct library depending on env vartiables describing the EPD size
screen_model = cfg.baedge["screen"]["model"]
screen_revision = cfg.baedge["screen"]["revision"]

epd_lib = importlib.import_module("lib.waveshare_epd.epd" + screen_model + screen_revision)
hlp.log_debug(__name__, '[config] load EPD Library for Model ' + screen_model + ' (Rev: ' + screen_revision + ')')


def initialize_screen():
    """ initialize eInk screen """
    hlp.log_debug('initialize_screen', 'init')

    try:
        epd = epd_lib.EPD()

        # TODO: remove or use
        # font = ImageFont.truetype(FONT_FACE, FONT_SIZE)

        hlp.log_debug('initialize_screen', 'initialize screen')
        epd.init()

        hlp.log_debug('initialize_screen', 'clear screen')
        epd.Clear()

        # 255 = clear background frame
        # image = Image.new('1', (epd.height, epd.width), 255)
        # draw = ImageDraw.Draw(image)
        # draw.text((cfg.coordinates.qrcode), text, font=font, fill=0)

        # epd.display_Base(epd.getbuffer(image))
        # epd.sleep()

        hlp.log_debug('initialize_screen', 'end')
        return epd

    except IOError as e:
        hlp.log_exception('initialize_screen', e)
        return None


def clear_screen(epd, sleep):
    """ clear content of eInk screen """
    hlp.log_debug('clear_screen', 'init')

    try:
        hlp.log_debug('clear_screen', 'clear screen')
        epd.Clear()

        # only sleep if requested
        if sleep:
            hlp.log_debug('clear_screen', 'sleep screen')
            epd.sleep()

        hlp.log_debug('clear_screen', 'end')
        return True

    except IOError as e:
        hlp.log_exception('clear_screen', e)
        return None


def write_socials_info(epd):
    """ write socials info to eInk screen """
    hlp.log_debug('write_socials_info', 'init')

    text = cfg.wearer["name"] + "\n" + cfg.wearer["title"] + "\n" + cfg.wearer["social"]

    try:
        font = ImageFont.truetype(FONT_FACE, FONT_SIZE)

        # 255 = clear background frame
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)
        draw.text((cfg.baedge["coordinates"]["qrcode"]), text, font=font, fill=0)

        hlp.log_debug('write_socials_info', 'generate QR code')
        qr = qrcode.QRCode(version=1, box_size=4)
        qr.add_data(cfg.wearer["link"])
        qr.make(fit=True)
        qrcode_image = qr.make_image()

        hlp.log_debug('write_socials_info', 'QR code image: ' + qrcode_image)
        image.paste(qrcode_image, (120, 60))

        epd.display(epd.getbuffer(image))

        # TODO: should we remove this?
        # hlp.log_debug('write_socials_info', 'sleep screen')
        # epd.sleep()

        hlp.log_debug('write_socials_info', 'end')
        return True

    except IOError as e:
        hlp.log_exception('write_socials_info', e)
        return None


def write_baedge_info(epd):
    """ write Baedge info to eInk screen """
    hlp.log_debug('write_baedge_info', 'init')

    # TODO: move this up and define more globally
    text = "{Ba,e}dge\n workloads.io/baedge "

    try:
        font = ImageFont.truetype(FONT_FACE, FONT_SIZE)

        # 255 = clear background frame
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        draw.text((cfg.baedge["coordinates"]["qrcode"]), text, font=font, fill=0)

        epd.display(epd.getbuffer(image))

        logging.debug("[write_baedge_info] sleep screen")
        # epd.sleep()

        hlp.log_debug('write_baedge_info', 'end')
        return True

    except IOError as e:
        hlp.log_exception('write_baedge_info', e)
        return None


def write_nomad_info(epd):
    """ write Nomad info to eInk screen """
    hlp.log_debug('write_nomad_info', 'init')

    try:
        font = ImageFont.truetype(FONT_FACE, FONT_SIZE)

        # TODO: move this up and define more globally
        text = cfg.nomad["allocation"] + "\n" + cfg.nomad["address"]

        nimage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(nimage)

        # header, containing HashiCorp logo + white "Nomad" text on a black banner
        # TODO: move this up and define more globally
        company_icon = Image.open(cfg.media["company_icon"])

        nimage.paste(company_icon, (0, 0))

        # draw a black rectangle on the top
        draw.rectangle((32, 0, 750, 31), fill=0)

        # write out Nomad in white
        draw.text((40, 0), "Nomad", font=font, fill=255)

        # write out Nomad info in black
        draw.text((0, 50), text, font=font, fill=0)

        # write to screen
        epd.display(epd.getbuffer(nimage))

        # hlp.log_debug('write_nomad_info', 'sleep screen')
        # epd.sleep()

        hlp.log_debug('write_nomad_info', 'end')
        return True

    except IOError as e:
        hlp.log_exception('write_nomad_info', e)
        return None


def write_text(epd, text, style):
    """ write textual content to eInk screen """
    hlp.log_debug('write_text', 'init')

    hlp.log_debug('write_text', 'text: ' + text)
    hlp.log_debug('write_text', 'style: ' + style)

    # TODO: move this up and define more globally
    font = ImageFont.truetype(FONT_FACE, FONT_SIZE)

    try:
        epd.init()
        # epd.Clear()

        image = Image.new('1', (epd.height, epd.width), 255)

        draw = ImageDraw.Draw(image)
        draw.text((5, 60), text, font=font, fill=0)

        epd.display(epd.getbuffer(image))

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

        hlp.log_debug('write_text', 'end')
        return True

    except IOError as e:
        hlp.log_exception('write_text', e)
        return None


def write_image(epd, image):
    """ write image content to eInk screen """
    hlp.log_debug('write_image', 'init')

    hlp.log_debug('write_image', 'image: ' + image)

    try:
        # TODO: implement image writing
        hlp.log_debug('write_image', 'not implemented')

        hlp.log_debug('write_image', 'end')
        return True

    except IOError as e:
        hlp.log_exception('write_image', e)
        return None
