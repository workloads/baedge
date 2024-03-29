""" Flask-based HTTP Server for Baedge API """

import logging
import os
import signal
import sys

from flask import (
    Flask,
    jsonify,
    make_response,
    render_template,
    request,
    send_from_directory
)

import helpers as hlp
import config as cfg
import baedge

# override server debug mode if log level is explicitly set to `DEBUG`
if cfg.app["logging"]["level"] == "DEBUG":
    cfg.app["debug"] = True

# enable application logging at the specified level
logging.basicConfig(level=cfg.app["logging"]["level"])

# toggle Flask's Werkzeug-specific logging
log = logging.getLogger('werkzeug')

if cfg.app["logging"]["werkzeug"]["enable"]:
    log.setLevel(cfg.app["logging"]["werkzeug"]["level"])
    log.disabled = False

else:
    log.disabled = True


# pylint: disable=unused-argument
def handle_signal(signal_name, signal_frame):
    """
    Handle System Signal and attempt graceful shutdown.

    Parameters:
        signal_name  (int):    A signal identifier.
        signal_frame (object): A signal frame.

    Returns:
        n/a
    """

    hlp.log_debug('handle_signal', 'catch signal `' + str(signal_name) + '`, attempt graceful shutdown')

    # attempt to clear the screen without sleeping to allow for releasing GPIO
    baedge.clear_screen(
        server.epd,
        sleep_screen=False
    )

    # release GPIO and exit EPD module cleanly
    baedge.epd_library.epdconfig.module_exit(cleanup=True)

    # good goodbye
    sys.exit(0)


# load Flask and disable wildcard static file serving
server = Flask(
    __name__,
    static_url_path='',
    static_folder=cfg.app["static_files"],
    template_folder=cfg.app["templates"],
)


@server.route(cfg.routes["root"], methods=['GET'])
def root_get():
    """ root endpoint """
    hlp.log_debug('GET ' + cfg.routes["root"], 'init')

    # render template and return status 200
    return render_template(
        'index.html',
        title=cfg.app["name"],
        description=cfg.app["description"],
        prefix=cfg.app["prefix"],
        routes=ROUTES,
    ), 200


# handle favicon-like requests, see https://flask.palletsprojects.com/en/3.0.x/patterns/favicon/
@server.route(cfg.routes["apple-touch-icon"])
def apple_touch_icon():
    """ apple-touch-icon endpoint """
    hlp.log_debug('GET ' + cfg.routes["apple-touch-icon"], 'init')

    # render file and return default status
    # see https://flask.palletsprojects.com/en/3.0.x/api/#flask.send_from_directory
    return send_from_directory(
        as_attachment=False,
        directory=cfg.app["static_files"] + "/images",
        etag=True,
        mimetype='image/png',
        path=cfg.media["web"]["apple-touch-icon"],
    )


# handle favicon-like requests, see https://flask.palletsprojects.com/en/3.0.x/patterns/favicon/
@server.route(cfg.routes["favicon"])
def favicon():
    """ favicon endpoint """
    hlp.log_debug('GET ' + cfg.routes["favicon"], 'init')

    # render file and return default status
    # see https://flask.palletsprojects.com/en/3.0.x/api/#flask.send_from_directory
    return send_from_directory(
        as_attachment=False,
        directory=cfg.app["static_files"] + "/images",
        etag=True,
        mimetype='image/vnd.microsoft.icon',
        path=cfg.media["web"]["favicon"],
    )


@server.route(cfg.routes["status"], methods=['GET'])
def status_get():
    """ status endpoint """
    hlp.log_debug('GET ' + cfg.routes["status"], 'init')

    return make_response("OK", 200)


@server.route(cfg.routes["status_environment"], methods=['GET'])
def status_environment_get():
    """ environment status endpoint """
    hlp.log_debug('GET ' + cfg.routes["status_environment"], 'init')

    # iterate over environment variables and build a string
    environment_info = ""

    for key, value in os.environ.items():
        environment_info += f"{key}: {value}<br>"

    # render environment info and return status 200
    return make_response(environment_info, 200)


@server.route(cfg.routes["status_routes"])
def status_routes_get():
    """ route status endpoint """
    hlp.log_debug('GET ' + cfg.routes["status_routes"], 'init')

    # render route info and return status 200
    return make_response(jsonify(ROUTES), 200)


@server.route(cfg.routes["status_screen"], methods=['GET'])
def status_screen_get():
    """ screen status endpoint """
    hlp.log_debug('GET ' + cfg.routes["status_screen"], 'init')

    # render message and return status 200
    return make_response("Device Status may be OK", 200)


@server.route(cfg.routes["device_clear"], methods=['POST'])
def clear_post():
    """ screen-clearing endpoint """
    hlp.log_debug('POST ' + cfg.routes["device_clear"], 'init')

    # baedge.clear_screen(server.epd, sleep=True)

    return make_response("OK", 200)


@server.route(cfg.routes["device_write"], methods=['POST'])
def write_post():
    """ screen-writing endpoint """
    hlp.log_debug('POST ' + cfg.routes["device_write"], 'init')

    # get `screen` identifier from POST data
    screen = request.form.get('screen')

    if screen:
        hlp.log_debug('POST ' + cfg.routes["device_write"], "screen is: " + screen)

        # catch disallowed screens and bail
        if screen not in cfg.screens["active"]:
            hlp.log_debug('POST ' + cfg.routes["device_write"], "select inactive screen")
            response = make_response("Cannot load screen `" + screen + "`", 400)

        # continue for allowed screens
        else:
            if baedge.write_screen(server.epd, screen):
                hlp.log_debug('POST ' + cfg.routes["device_write"], "write to screen successful")
                response = make_response("OK", 200)

            else:
                hlp.log_debug('POST ' + cfg.routes["device_write"], "write to screen failed")
                response = make_response("Unable to write to screen", 400)

    else:
        response = make_response("Payload did not contain expected data", 400)

    return response


# assemble formatted route map
# MUST BE defined after all routes have been added
ROUTES = hlp.format_url_map(
    url_map=server.url_map.iter_rules(),
    hidden_routes=cfg.routes["hidden_routes"],
    visible_methods=cfg.routes["visible_methods"],
    visible_prefix=cfg.app["prefix"],
)

# if no app name is specified, default to running Flask internally
if __name__ == "__main__":
    hlp.log_debug(__name__, 'initialize function')

    # skip screen initialization if an unsupported OS is detected:
    if not baedge.SKIP_INITIALIZE_SCREEN:
        # initialize eInk screen
        hlp.log_debug(__name__, 'initialize screen')
        server.epd = baedge.initialize_screen()

        hlp.log_debug(__name__, 'write initial screen: ' + cfg.baedge["initial_screen"])
        baedge.write_screen(server.epd, cfg.baedge["initial_screen"])

    else:
        hlp.log_debug(__name__, 'skip screen initialization')

    # catch system signals and (attempt to) handle them gracefully
    # SIGKILL and SIGSTOP cannot be caught, blocked, or ignored
    # see https://docs.python.org/3/library/signal.html
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    # start Flask application
    hlp.log_info(__name__, 'start server at http://' + cfg.app["host"] + ":" + str(cfg.app["port"]))
    server.run(
        debug=cfg.app["debug"],
        host=cfg.app["host"],
        port=cfg.app["port"],
        load_dotenv=cfg.app["load_dotenv"],

        # using Flask's reloader functionality is highly likely to cause issues with several Waveshare eInk screen models
        # as the reloader bypasses the required screen sleep and initialization steps, resulting in `GPIO busy` errors.
        use_reloader=False
    )
