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


def write_text(epd, text, style):
    """ write textual content to eInk screen """
    hlp.log_debug('write_text', 'init')

    hlp.log_debug('write_text', 'text: ' + text)
    hlp.log_debug('write_text', 'style: ' + style)

    # to do: move this up and define more globally
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


def write_image(image):
    """ write image content to eInk screen """
    hlp.log_debug('write_image', 'init')

    hlp.log_debug('write_image', 'image: ' + image)

    try:
        # to do: implement image writing
        hlp.log_debug('write_image', 'not implemented')

        hlp.log_debug('write_image', 'end')
        return True

    except IOError as e:
        hlp.log_exception('write_image', e)
        return None


def write_baedge_info(epd):
    """ write Baedge info to eInk screen """
    hlp.log_debug('write_baedge_info', 'init')

    # to do: move this up and define more globally
    text = "{Ba,e}dge\n go.workloads.io/baedge"

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

        # to do: move this up and define more globally
        text = cfg.nomad["allocation"] + "\n" + cfg.nomad["address"]

        nimage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(nimage)

        # header, containing HashiCorp logo + white "Nomad" text on a black banner
        # to do: move this up and define more globally
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
