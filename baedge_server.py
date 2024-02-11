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
app = Flask(__name__, static_folder=None)

# initialize eInk screen
app.epd = baedge.initialize_screen()


@app.route("/", methods=['GET'])
def root_get():
    """ root endpoint """
    hlp.log_debug('GET /', 'init')

    response = make_response(APP_NAME, 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_STATUS, methods=['GET'])
def status_get():
    """ health endpoint """
    hlp.log_debug('GET /status', 'init')

    response = make_response("OK", 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_STATUS + "/environment", methods=['GET'])
def status_environment_get():
    """ environment endpoint """
    hlp.log_debug('GET /status/environment', 'init')

    # iterate over environment variables and build a string
    environment_info = ""
    for key, value in os.environ.items():
        environment_info += f"{key}: {value}<br>"

    response = make_response(environment_info, 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_STATUS + "/routes")
def status_routes_get():
    """ route status endpoint """
    hlp.log_debug('GET /status/routes', 'init')

    route_list = []

    for route in app.url_map.iter_rules():
        methods = ', '.join(route.methods)

        route_list.append({
            'function': route.endpoint,
            'methods': methods,
            'path': str(route),
        })

    response = make_response(jsonify(route_list), 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_STATUS + "/screen", methods=['GET'])
def status_screen_get():
    """ screen status endpoint """
    hlp.log_debug('GET /status/screen', 'init')

    response = make_response("Device Status may be OK", 200)

    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_DEVICE + "/clear", methods=['POST'])
def clear_post():
    """ screen-clearing endpoint """
    hlp.log_debug('POST /device/clear', 'init')

    baedge.clear_screen(app.epd, sleep=True)

    # respond with status code and message
    response = make_response("OK", 200)
    return response


@app.route(ROUTE_API_VERSION + ROUTE_NAMESPACE_DEVICE + "/write", methods=['POST'])
def write_post():
    """ screen-writing endpoint """
    hlp.log_debug('POST /device/write', 'init')

    # get data from request and parse as JSON
    data = request.get_json(force=True)

    if data.get('text'):
        hlp.log_debug('POST /device/write', 'write text to screen')
        baedge.write_text(app.epd, data.get('text'), data.get('style'))

        response = make_response("OK", 200)

    elif data.get('image'):
        hlp.log_debug('POST /device/write', 'write image to screen')
        baedge.write_image(app.epd, data.get('image'))

        response = make_response("OK", 200)

    else:
        hlp.log_error('POST /device/write', 'unable to write to screen')

        response = make_response("Payload did not contain expected data", 400)

    return response


# if no app name is specified, default to running Flask internally
if __name__ == "__main__":
    # app.epd = baedge.initialize_screen()
    app.run(host=server_host, port=server_port, debug=DEBUG_MODE, load_dotenv=DOTENV)
