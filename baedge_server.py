""" Flask-based HTTP Server for Baedge API """

import os
import logging

from flask import Flask, jsonify, make_response, request

import baedge
import helpers as hlp
import config as cfg

# override server debug mode if log level is explicitly set to `DEBUG`
if cfg.app["log_level"] == "DEBUG":
    cfg.app["debug"] = True

# enable logging at the specified level
logging.basicConfig(level=cfg.app["log_level"])

# load Flask and disable static file serving
server = Flask(__name__, static_folder=None)

# initialize eInk screen
app.epd = baedge.initialize_screen()


@server.route(cfg.routes["root"], methods=['GET'])
def root_get():
    """ root endpoint """
    hlp.log_debug('GET ' + cfg.routes["root"], 'init')

    response = make_response(cfg.app["name"], 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_STATUS, methods=['GET'])
def status_get():
    """ status endpoint """
    hlp.log_debug('GET ' + cfg.routes["status"], 'init')

    response = make_response("OK", 200)
    return response


@server.route(cfg.routes["status_environment"], methods=['GET'])
def status_environment_get():
    """ environment status endpoint """
    hlp.log_debug('GET ' + cfg.routes["status_environment"], 'init')

    # iterate over environment variables and build a string
    environment_info = ""

    for key, value in os.environ.items():
        environment_info += f"{key}: {value}<br>"

    response = make_response(environment_info, 200)
    return response


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

    response = make_response(jsonify(route_list), 200)
    return response


@server.route(cfg.routes["status_screen"], methods=['GET'])
def status_screen_get():
    """ screen status endpoint """
    hlp.log_debug('GET ' + cfg.routes["status_screen"], 'init')

    response = make_response("Device Status may be OK", 200)
    return response


@server.route(cfg.routes["device_clear"], methods=['POST'])
def clear_post():
    """ screen-clearing endpoint """
    hlp.log_debug('POST ' + cfg.routes["device_clear"], 'init')

    # baedge.clear_screen(server.epd, sleep=True)

    # respond with status code and message
    response = make_response("OK", 200)
    return response


@server.route(cfg.routes["device_write"], methods=['POST'])
def write_post():
    """ screen-writing endpoint """
    hlp.log_debug('POST ' + cfg.routes["device_write"], 'init')

    # get data from request and parse as JSON
    data = request.get_json(force=True)

    if data.get('text'):
        hlp.log_debug('POST ' + cfg.routes["device_write"], 'write text to screen')
        # baedge.write_text(server.epd, data.get('text'), data.get('style'))

        response = make_response("OK", 200)

    elif data.get('image'):
        hlp.log_debug('POST ' + cfg.routes["device_write"], 'write image to screen')
        # baedge.write_image(server.epd, data.get('image'))

        response = make_response("OK", 200)

    else:
        hlp.log_error('POST ' + cfg.routes["device_write"], 'unable to write to screen')

        response = make_response("Payload did not contain expected data", 400)

    return response


# if no app name is specified, default to running Flask internally
if __name__ == "__main__":
    hlp.log_debug(__name__, 'init Flask')

    # TODO: should we remove this?
    # server.epd = baedge.initialize_screen()

    # start Flask application
    server.run(
      debug=cfg.app["debug"],
      host=cfg.app["host"],
      port=cfg.app["port"],
      load_dotenv=cfg.app["dotenv"]
    )
