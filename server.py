""" Flask-based HTTP Server for Baedge API """

import os
import logging

from flask import Flask, jsonify, make_response, render_template, request, send_from_directory

import helpers as hlp
import config as cfg
import baedge

# override server debug mode if log level is explicitly set to `DEBUG`
if cfg.app["logging"]["level"] == "DEBUG":
    cfg.app["debug"] = True

# enable application logging at the specified level
logging.basicConfig(level=cfg.app["logging"]["level"])

# toggle Flask;s Werkzeug-specific logging
log = logging.getLogger('werkzeug')

if cfg.app["logging"]["werkzeug"]["enable"]:
    log.setLevel(cfg.app["logging"]["werkzeug"]["level"])
    log.disabled = False

else:
    log.disabled = True

# load Flask and disable wildcard static file serving
server = Flask(
    __name__,
    static_folder=None,
    template_folder=cfg.app["templates"],
  )

# initialize eInk screen
# server.epd = baedge.initialize_screen()


@server.route(cfg.routes["root"], methods=['GET'])
def root_get():
    """ root endpoint """
    hlp.log_debug('GET ' + cfg.routes["root"], 'init')

    # render template and return status 200
    return render_template(
      'index.html',
      title=cfg.app["name"],
      description=cfg.app["description"],

      # `logo_path` must be a path that is actually routed
      logo_path="/" + cfg.media["web"]["favicon"],
      logo_alt_text=cfg.app["description"],
    ), 200


# handle favicon-like resend_from_directoryquests, see https://flask.palletsprojects.com/en/3.0.x/patterns/favicon/
@server.route(cfg.routes["apple-touch-icon"])
def apple_touch_icon():
    """ apple-touch-icon endpoint """
    hlp.log_debug('GET ' + cfg.routes["apple-touch-icon"], 'init')

    # render file and return default status
    return send_from_directory(
      as_attachment=False,
      directory=cfg.media["web"]["images"],
      path=cfg.media["web"]["apple-touch-icon"],
    )


# handle favicon-like resend_from_directoryquests, see https://flask.palletsprojects.com/en/3.0.x/patterns/favicon/
@server.route(cfg.routes["favicon"])
def favicon():
    """ favicon endpoint """
    hlp.log_debug('GET ' + cfg.routes["favicon"], 'init')

    # render file and return default status
    return send_from_directory(
      as_attachment=False,
      directory=cfg.app["media"],
      path=cfg.media["web"]["favicon"],
      mimetype='image/vnd.microsoft.icon'
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

    route_list = []

    for route in server.url_map.iter_rules():
        methods = ', '.join(route.methods)

        route_list.append({
            'function': route.endpoint,
            'methods': methods,
            'path': str(route),
        })

    # render route info and return status 200
    return make_response(jsonify(route_list), 200)


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
        if screen not in cfg.screens["allowed"]:
            hlp.log_debug('POST ' + cfg.routes["device_write"], "select inactive screen")
            response = make_response("Not allowed to load screen `" + screen + "`", 400)

        if baedge.write_screen(server.epd, screen, sleep_screen=False):
            hlp.log_debug('POST ' + cfg.routes["device_write"], "write to screen successful")
            response = make_response("OK", 200)

        else:
            hlp.log_debug('POST ' + cfg.routes["device_write"], "write to screen failed")
            response = make_response("Unable to write to screen", 400)

    else:
        response = make_response("Payload did not contain expected data", 400)

    return response


# if no app name is specified, default to running Flask internally
if __name__ == "__main__":
    hlp.log_debug(__name__, 'init Flask')

    hlp.log_debug(__name__, 'initialize screen')
    server.epd = baedge.initialize_screen()

    # start Flask application
    server.run(
      debug=cfg.app["debug"],
      host=cfg.app["host"],
      port=cfg.app["port"],
      load_dotenv=cfg.app["dotenv"]
    )
